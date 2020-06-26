from oscar.apps.checkout.session import CheckoutSessionMixin as CoreCheckoutSessionMixin
from decimal import Decimal as D
from oscar.core.loading import get_class


Repository = get_class('shipping.repository', 'Repository')


class CheckoutSessionMixin(CoreCheckoutSessionMixin):

    def build_submission(self, **kwargs):
        """
        Return a dict of data that contains everything required for an order
        submission.  This includes payment details (if any).

        This can be the right place to perform tax lookups and apply them to
        the basket.
        """
        # Pop the basket if there is one, because we pass it as a positional
        # argument to methods below
        basket = kwargs.pop('basket', self.request.basket)
        shipping_address = self.get_shipping_address(basket)
        shipping_method = self.get_shipping_method(
            basket, shipping_address)
        billing_address = self.get_billing_address(shipping_address)
        if not shipping_method:
            total = shipping_charge = None
        else:
            shipping_charge = shipping_method.calculate(basket)

            total = self.get_order_totals(basket, shipping_charge=shipping_charge, **kwargs)

        submission = {
            'user': self.request.user,
            'basket': basket,
            'shipping_address': shipping_address,
            'shipping_method': shipping_method,
            'shipping_charge': shipping_charge,
            'billing_address': billing_address,
            'order_total': total,
            'order_kwargs': {},
            'payment_kwargs': {}}

        # add extra setting for mix baskets
        try:
            submission['order_total_mix'] = total['parent']
        except:
            pass

        # If there is a billing address, add it to the payment kwargs as calls
        # to payment gateways generally require the billing address. Note, that
        # it normally makes sense to pass the form instance that captures the
        # billing address information. That way, if payment fails, you can
        # render bound forms in the template to make re-submission easier.
        if billing_address:
            submission['payment_kwargs']['billing_address'] = billing_address

        # Allow overrides to be passed in
        submission.update(kwargs)

        # Set guest email after overrides as we need to update the order_kwargs
        # entry.
        user = submission['user']
        if (not user.is_authenticated
                and 'guest_email' not in submission['order_kwargs']):
            email = self.checkout_session.get_guest_email()
            submission['order_kwargs']['guest_email'] = email
        return submission


    def skip_unless_payment_is_required(self, request):
        # Check to see if payment is actually required for this order.
        shipping_address = self.get_shipping_address(request.basket)
        shipping_method = self.get_shipping_method(
            request.basket, shipping_address)
        if shipping_method:
            shipping_charge = shipping_method.calculate(request.basket)
        else:
            # It's unusual to get here as a shipping method should be set by
            # the time this skip-condition is called. In the absence of any
            # other evidence, we assume the shipping charge is zero.
            shipping_charge = prices.Price(
                currency=request.basket.currency, excl_tax=D('0.00'),
                tax=D('0.00')
            )

        total = self.get_order_totals(request.basket, shipping_charge)

        if request.basket.is_multi_partner:
            if total['parent'].excl_tax == D('0.00'):
                raise exceptions.PassedSkipCondition(
                    url=reverse('checkout:preview')
                )
        else:
            if total.excl_tax == D('0.00'):
                raise exceptions.PassedSkipCondition(
                    url=reverse('checkout:preview')
                )

    def get_shipping_method(self, basket, shipping_address=None, **kwargs):
        """
        Return the selected shipping method instance from this checkout session

        The shipping address is passed as we need to check that the method
        stored in the session is still valid for the shipping address.
        """
        code = self.checkout_session.shipping_method_code(basket)


        methods = Repository().get_shipping_methods(
            basket=basket, user=self.request.user,
            shipping_addr=shipping_address, request=self.request)

        # print(methods)

        #
        # for partner, method_list in methods.items():
        #     if method.code == code:
        #         return method
