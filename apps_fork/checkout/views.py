from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from django.views import generic
from oscar.core.loading import get_class
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect


CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
ShippingMethodForm = get_class('checkout.forms', 'ShippingMethodForm')
Repository = get_class('shipping.repository', 'Repository')


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
        submissions = self.build_submission()
        # delete setting added only for template for mix baskets
        submissions.pop("order_total_mix", None)
        return self.submit(**submissions)


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
    success_url = reverse_lazy('checkout:payment-method')

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
