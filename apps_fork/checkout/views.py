import logging

from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from django.views import generic
from oscar.core.loading import get_class
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import gettext as _


from django.conf import settings
from decimal import Decimal
from oscar.core.loading import get_model

from oscar.apps.checkout import signals

basket = get_model('basket', 'Basket')
blogprojet = get_model('blog', 'BlogProjet')
donation = get_model('order', 'Donation')
order = get_model('order', 'Order')

CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
ShippingMethodForm = get_class('checkout.forms', 'ShippingMethodForm')
Repository = get_class('shipping.repository', 'Repository')

# Standard logger for checkout events
logger = logging.getLogger('oscar.checkout')


class PaymentDetailsView(CorePaymentDetailsView):


    def handle_place_order_submission(self, request):
        """
        Handle a request to place an order.

        This method is normally called after the customer has clicked "place
        order" on the preview page. It's responsible for (re-)validating any
        form information then building the submission dict to pass to the
        `submit` method.

        If forms are submitted on your payment details view, you should
        override this method to ensure they are valid before extracting their
        data into the submission dict and passing it onto `submit`.
        """
        ctx = self.get_context_data()
        submissions = self.build_submission()
        # add project donation details
        submissions['order_kwargs'] = {'project': ctx['basket'].project, 'donation': ctx['donation']}
        
        # delete setting added only for template for mix baskets
        submissions.pop("order_total_mix", None)

        return self.submit(**submissions)
        
    def render_preview(self, request, **kwargs):
        """
        Show a preview of the order.

        If sensitive data was submitted on the payment details page, you will
        need to pass it back to the view here so it can be stored in hidden
        form inputs.  This avoids ever writing the sensitive data to disk.
        """
        self.preview = True
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('pid', '') != '':
            project_id = self.request.GET.get('pid', '')
            t_basket = basket.objects.get(pk=context['basket'].pk)
            t_basket.set_project(project_id)
            
        context['donation'] = self.get_donation_amount(context)
        return context
        
    def get_donation_amount(self, context):
        # Calculates amount that will be given to the project
        rate = settings.TAUTOKO_RATE_OF_DONATION

        if context['basket'].is_multi_partner:
            return round(context['order_total']['parent'].incl_tax * Decimal(rate), 2)
        else:
            return round(context['order_total'].incl_tax * Decimal(rate), 2)
        
    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
               shipping_charge, billing_address, order_total,
               payment_kwargs=None, order_kwargs=None):
        """
        Submit a basket for order placement.

        The process runs as follows:

         * Generate an order number
         * Freeze the basket so it cannot be modified any more (important when
           redirecting the user to another site for payment as it prevents the
           basket being manipulated during the payment process).
         * Attempt to take payment for the order
           - If payment is successful, place the order
           - If a redirect is required (e.g. PayPal, 3D Secure), redirect
           - If payment is unsuccessful, show an appropriate error message

        :basket: The basket to submit.
        :payment_kwargs: Additional kwargs to pass to the handle_payment
                         method. It normally makes sense to pass form
                         instances (rather than model instances) so that the
                         forms can be re-rendered correctly if payment fails.
        :order_kwargs: Additional kwargs to pass to the place_order method
        """
        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}

        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_charge.is_tax_known, (
            "Shipping charge tax must be set before a user can place an order")

        # We generate the order number first as this will be used
        # in payment requests (ie before the order model has been
        # created).  We also save it in the session for multi-stage
        # checkouts (e.g. where we redirect to a 3rd party site and place
        # the order on a different request).
        order_number = self.generate_order_number(basket)
        self.checkout_session.set_order_number(order_number)
        logger.info("Order #%s: beginning submission process for basket #%d",
                    order_number, basket.id)

        # Freeze the basket so it cannot be manipulated while the customer is
        # completing payment on a 3rd party site.  Also, store a reference to
        # the basket in the session so that we know which basket to thaw if we
        # get an unsuccessful payment response when redirecting to a 3rd party
        # site.
        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        error_msg = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")

        signals.pre_payment.send_robust(sender=self, view=self)

        try:
            self.handle_payment(order_number, order_total, **payment_kwargs)
        except RedirectRequired as e:
            # Redirect required (e.g. PayPal, 3DS)
            logger.info("Order #%s: redirecting to %s", order_number, e.url)
            return http.HttpResponseRedirect(e.url)
        except UnableToTakePayment as e:
            # Something went wrong with payment but in an anticipated way.  Eg
            # their bankcard has expired, wrong card number - that kind of
            # thing. This type of exception is supposed to set a friendly error
            # message that makes sense to the customer.
            msg = str(e)
            logger.warning(
                "Order #%s: unable to take payment (%s) - restoring basket",
                order_number, msg)
            self.restore_frozen_basket()

            # We assume that the details submitted on the payment details view
            # were invalid (e.g. expired bankcard).
            return self.render_payment_details(
                self.request, error=msg, **payment_kwargs)
        except PaymentError as e:
            # A general payment error - Something went wrong which wasn't
            # anticipated.  Eg, the payment gateway is down (it happens), your
            # credentials are wrong - that king of thing.
            # It makes sense to configure the checkout logger to
            # mail admins on an error as this issue warrants some further
            # investigation.
            msg = str(e)
            logger.error("Order #%s: payment error (%s)", order_number, msg,
                         exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)
        except Exception as e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development...
            logger.error(
                "Order #%s: unhandled exception while taking payment (%s)",
                order_number, e, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)

        signals.post_payment.send_robust(sender=self, view=self)

        # If all is ok with payment, try and place order
        logger.info("Order #%s: payment successful, placing order",
                    order_number)
        try:
            return self.handle_order_placement(
                order_number, user, basket, shipping_address, shipping_method,
                shipping_charge, billing_address, order_total, **order_kwargs)
        except UnableToPlaceOrder as e:
            # It's possible that something will go wrong while trying to
            # actually place an order.  Not a good situation to be in as a
            # payment transaction may already have taken place, but needs
            # to be handled gracefully.
            msg = str(e)
            logger.error("Order #%s: unable to place order - %s",
                         order_number, msg, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=msg, **payment_kwargs)
              



class ShippingMethodView(CheckoutSessionMixin, generic.FormView):
    """
    View for allowing a user to choose a shipping method.

    Shipping methods are largely domain-specific and so this view
    will commonly need to be subclassed and customised.

    The default behaviour is to load all the available shipping methods
    using the shipping Repository.  If there is only 1, then it is
    automatically selected.  Otherwise, a page is rendered where
    the user can choose the appropriate one.
    """
    template_name = 'oscar/checkout/shipping_methods.html'
    form_class = ShippingMethodForm

    pre_conditions = ['check_basket_is_not_empty',
                      'check_basket_is_valid',
                      'check_user_email_is_captured']
    success_url = reverse_lazy('checkout:project-choice')

    def post(self, request, *args, **kwargs):

        # concatenate data for form from POST request and from methods
        data_form = {}
        data_form.update(self.initial())
        data_form.update(request.POST.dict())

        form = self.form_class(data_form, extra = self.get_available_shipping_methods())
        if form.is_valid():
            self.checkout_session.use_shipping_method(form.clean())

        #return self.get_success_response()
        # return super().get_success_url()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        # These pre-conditions can't easily be factored out into the normal
        # pre-conditions as they do more than run a test and then raise an
        # exception on failure.

        # Check that shipping is required at all
        if not request.basket.is_shipping_required():
            # No shipping required - we store a special code to indicate so.
            self.checkout_session.use_shipping_method(
                NoShippingRequired().code)
            return self.get_success_response()

        # Check that shipping address has been completed
        if not self.checkout_session.is_shipping_address_set():
            messages.error(request, _("Please choose a shipping address"))
            return redirect('checkout:shipping-address')

        # Save shipping methods as instance var as we need them both here
        # and when setting the context vars.
        self._methods = self.get_available_shipping_methods()


        if len(self._methods) == 0:
            # No shipping methods available for given address
            messages.warning(request, _(
                "Shipping is unavailable for your chosen address - please "
                "choose another"))
            return redirect('checkout:shipping-address')


        # Must be more than one available shipping method, we present them to
        # the user to make a choice.
        form = self.form_class(initial = self.initial(), extra = self.get_available_shipping_methods())
        # return super().get(request, *args, **kwargs)
        return TemplateResponse(request, self.template_name, {'methods': self._methods, 'form': form})

    def initial(self):
        # return initial data for shipping form
        data = {}
        i=0
        for partner, method_list in self.get_available_shipping_methods().items():
            data[f'method_partner_name_{i}'] = partner.name
            data[f'method_partner_id_{i}'] = partner.id
            i += 1
        return data


    def get_available_shipping_methods(self):
        """
        Returns all applicable shipping method objects for a given basket.
        """
        # Shipping methods can depend on the user, the contents of the basket
        # and the shipping address (so we pass all these things to the
        # repository).  I haven't come across a scenario that doesn't fit this
        # system.
        return Repository().get_shipping_methods(
            basket=self.request.basket, user=self.request.user,
            shipping_addr=self.get_shipping_address(self.request.basket),
            request=self.request)


    def get_success_response(self):
        return redirect(self.success_url)
        
        
class ProjectChoiceView(CheckoutSessionMixin, generic.ListView):
    """
    view that allows customer to pick a project he wish to fund during checkout
    """
    model = blogprojet
    template_name = 'oscar/checkout/project_choice.html'
    pre_conditions = ['check_basket_is_not_empty',
                  'check_basket_is_valid',
                  'check_user_email_is_captured']
    success_url = reverse_lazy('checkout:payment-method')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donation'] = self.get_donation_amount(context)
        return context
        
    def get_donation_amount(self, context):
        # Calculates amount that will be given to the project
        rate = settings.TAUTOKO_RATE_OF_DONATION

        if context['basket'].is_multi_partner:
            return round(context['order_total']['parent'].incl_tax * Decimal(rate), 2)
        else:
            return round(context['order_total'].incl_tax * Decimal(rate), 2)

    
    
    
    
