from oscar.apps.basket.views import BasketView as CoreBasketView
from oscar.core.loading import get_class

OrderTotalCalculator = get_class('checkout.calculators', 'OrderTotalCalculator')


class BasketView(CoreBasketView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voucher_form'] = self.get_basket_voucher_form()

        # Shipping information is included to give an idea of the total order
        # cost.  It is also important for PayPal Express where the customer
        # gets redirected away from the basket page and needs to see what the
        # estimated order total is beforehand.
        context['shipping_methods'] = self.get_shipping_methods(
            self.request.basket)
        method = self.get_default_shipping_method(self.request.basket)
        context['shipping_method'] = method
        shipping_charge = method.calculate(self.request.basket)
        context['shipping_charge'] = shipping_charge
        if method.is_discounted:
            excl_discount = method.calculate_excl_discount(self.request.basket)
            context['shipping_charge_excl_discount'] = excl_discount

        # Return right total according to mix baskets
        if self.request.basket.is_multi_partner:
            context['order_total'] = OrderTotalCalculator().calculate(
                self.request.basket, shipping_charge)['parent']
        else:
            context['order_total'] = OrderTotalCalculator().calculate(
                self.request.basket, shipping_charge)


        context['basket_warnings'] = self.get_basket_warnings(
            self.request.basket)
        context['upsell_messages'] = self.get_upsell_messages(
            self.request.basket)

        if self.request.user.is_authenticated:
            try:
                saved_basket = self.basket_model.saved.get(
                    owner=self.request.user)
            except self.basket_model.DoesNotExist:
                pass
            else:
                saved_basket.strategy = self.request.basket.strategy
                if not saved_basket.is_empty:
                    saved_queryset = saved_basket.all_lines()
                    formset = SavedLineFormSet(strategy=self.request.strategy,
                                               basket=self.request.basket,
                                               queryset=saved_queryset,
                                               prefix='saved')
                    context['saved_formset'] = formset
        return context
