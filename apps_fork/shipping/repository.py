from oscar.apps.shipping import repository
from apps_fork.shipping.methods import MainMethod
from apps_fork.shipping.models import ShippingRule

# class Repository(repository.Repository):
#     methods = (methods.Standard(), methods.Express())


class Repository(repository.Repository):

    def get_shipping_methods(self, basket, **kwargs):
        methods = []

        # loop on partners contened within the basket
        for partner in basket.partner_list:

            rule_set = []
            # loop within partner rules
            for rule in ShippingRule.objects.filter(partner=partner):

                methods.append(MainMethod(rule, basket))

        return methods

    def get_default_shipping_method(self, basket, shipping_addr=None,
                                    **kwargs):
        """
        Return a 'default' shipping method to show on the basket page to give
        the customer an indication of what their order will cost.
        """
        shipping_methods = self.get_shipping_methods(basket, **kwargs)
        if len(shipping_methods) == 0:
            raise ImproperlyConfigured(
                _("You need to define some shipping methods"))

        # Assume first returned method is default
        return shipping_methods[list(shipping_methods.keys())[0]][0]
