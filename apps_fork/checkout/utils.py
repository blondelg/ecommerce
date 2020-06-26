from oscar.apps.checkout.utils import CheckoutSessionData as CoreCheckoutSessionData


class CheckoutSessionData(CoreCheckoutSessionData):


    def shipping_method_code(self, basket):
        """
        Return the shipping method code
        """

        return self._get('shipping', 'method_code')

    def use_shipping_method(self, code):
        """
        Set shipping method code to session
        """
        self._set('shipping', 'method_code', code)
