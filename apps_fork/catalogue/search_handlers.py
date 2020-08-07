from django.conf import settings
from oscar.apps.catalogue.search_handlers import SimpleProductSearchHandler as CoreSimpleProductSearchHandler

from oscar.core.loading import get_class, get_model

BrowseCategoryForm = get_class('search.forms', 'BrowseCategoryForm')
SearchHandler = get_class('search.search_handlers', 'SearchHandler')
is_solr_supported = get_class('search.features', 'is_solr_supported')
is_elasticsearch_supported = get_class('search.features', 'is_elasticsearch_supported')
Product = get_model('catalogue', 'Product')
Tag = get_model('content', 'Tag')


class SimpleProductSearchHandler(CoreSimpleProductSearchHandler):
    """
    A basic implementation of the full-featured SearchHandler that has no
    faceting support, but doesn't require a Haystack backend. It only
    supports category browsing.

    Note that is meant as a replacement search handler and not as a view
    mixin; the mixin just does most of what we need it to do.
    
    Fork: add the possibility to filter by tags
    """
    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    def __init__(self, request_data, full_path, categories=None, tags=None):
        self.categories = categories
        self.tags = tags
        self.kwargs = {'page': request_data.get('page', 1)}
        self.object_list = self.get_queryset()

    def get_queryset(self):
        qs = Product.objects.browsable().base_queryset()
        if self.categories:
            qs = qs.filter(categories__in=self.categories).distinct()
        if self.tags:
            qs = qs.filter(tags__in=[self.tags]).distinct()

        return qs

    def get_search_context_data(self, context_object_name):
        # Set the context_object_name instance property as it's needed
        # internally by MultipleObjectMixin
        self.context_object_name = context_object_name
        context = self.get_context_data(object_list=self.object_list)
        context[context_object_name] = context['page_obj'].object_list

        return context
        
