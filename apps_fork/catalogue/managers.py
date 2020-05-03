from oscar.apps.catalogue.managers import ProductQuerySet as CoreProductQuerySet

class ProductQuerySet(CoreProductQuerySet):

    def browsable_dashboard(self):
        """
        Products that should be browsable in the dashboard.

        Excludes non-canonical products, but includes non-public products.
        """
        return self.filter()
