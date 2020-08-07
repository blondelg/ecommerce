from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from oscar.apps.catalogue.views import CatalogueView as CoreCatalogueView
from django.views.generic import TemplateView
from apps_fork.catalogue.signals import product_viewed
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.paginator import InvalidPage

from oscar.core.loading import get_class, get_model

Class = get_model('catalogue', 'productclass')
Tag = get_model('content', 'Tag')
get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')
    
    

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
        
class ProductTagView(TemplateView):
    """
    Browse products in a given product tag
    """
    context_object_name = "products"
    template_name = 'oscar/catalogue/browse.html'
    enforce_paths = True    
    
    def get(self, request, *args, **kwargs):
        try:
            self.search_handler = self.get_search_handler(self.request.GET, request.get_full_path(), categories=[], tags=self.get_tag())
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _('The given page number was invalid.'))
            return redirect('catalogue:index')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        
        ctx = {}
        ctx['summary'] = _(self.kwargs['tag'])
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name)
        ctx.update(search_context)
        return ctx
        
    def get_tag(self):
        return get_object_or_404(Tag, pk=self.kwargs['tag'])
        
    def get_search_handler(self, *args, **kwargs):
        return get_product_search_handler_class()(*args, **kwargs)

