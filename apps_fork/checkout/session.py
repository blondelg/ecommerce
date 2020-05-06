from oscar.apps.checkout.session import CheckoutSessionMixin as CoreCheckoutSessionMixin
from decimal import Decimal as D


class CheckoutSessionMixin(CoreCheckoutSessionMixin):

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

        # check multi partners
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
