from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from apps_fork.catalogue.signals import product_viewed

class ProductDetailView(CoreProductDetailView):
    view_signal = product_viewed

    def get_request(self):
        """ return request """
        return self.request
