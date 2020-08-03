from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from oscar.apps.catalogue.views import CatalogueView as CoreCatalogueView
from apps_fork.catalogue.signals import product_viewed

from oscar.core.loading import get_class, get_model

Class = get_model('catalogue', 'productclass')

class ProductDetailView(CoreProductDetailView):
    view_signal = product_viewed

    def get_request(self):
        """ return request """
        return self.request
        
class CatalogueView(CoreCatalogueView):

    """
    Browse all products in the catalogue
    """
    context_object_name = "products"
    template_name = 'oscar/catalogue/browse.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)        
        ctx['classes'] = Class.objects.all()
        return ctx
