from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from django.views import generic
from oscar.core.loading import get_class
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect


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
        self._methods = self.get_available_shipping_methods()
        return super().post(request, *args, **kwargs)

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
        elif len(self._methods) == 1:
            # Only one shipping method - set this and redirect onto the next
            # step
            self.checkout_session.use_shipping_method(self._methods[0].code)
            return self.get_success_response()

        # Must be more than one available shipping method, we present them to
        # the user to make a choice.
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['methods'] = self._methods
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['methods'] = self._methods
        return kwargs

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

    def form_valid(self, form):
        # Save the code for the chosen shipping method in the session
        # and continue to the next step.
        self.checkout_session.use_shipping_method(form.cleaned_data['method_code'])
        return self.get_success_response()

    def form_invalid(self, form):
        messages.error(self.request, _("Your submitted shipping method is not"
                                       " permitted"))
        return super().form_invalid(form)

    def get_success_response(self):
        return redirect(self.get_success_url())
