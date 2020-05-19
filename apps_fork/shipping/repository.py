from oscar.apps.shipping import repository
from . import methods
from apps_fork.shipping.models import ShippingRule

class Repository(repository.Repository):
    methods = (methods.Standard(), methods.Express())


# class Repository(repository.Repository):
#
#     def get_shipping_methods(self, basket, **kwargs):
#
#         pass
