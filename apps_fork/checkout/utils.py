from oscar.apps.checkout.utils import CheckoutSessionData as CoreCheckoutSessionData


class CheckoutSessionData(CoreCheckoutSessionData):


    def shipping_method_code(self, basket):
        """ generate a list of method codes, each code is the db method id """
        code_list = []
        try:
            for key, value in self._get('shipping', 'method_dict').items():
                if 'selected_method' in key:
                    code_list.append(int(value))
            return code_list
        except:
            return

    def use_shipping_method(self, method):
        """
        Set shipping method code to session
        """
        self._set('shipping', 'method_dict', method)
