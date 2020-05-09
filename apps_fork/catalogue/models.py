from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.utils.translation import gettext_lazy as _


class Product(AbstractProduct):

    partner = models.ForeignKey(
        'partner.Partner',
        on_delete=models.CASCADE,
        default=1,
        verbose_name=_("Partner"),
        related_name='products')

    @property
    def has_stockrecords(self):
        """
        Test if this product has any stockrecords
        """
        try:
            a=self.stockrecords.pk
            return True
        except:
            return False

    @property
    def stock_level(self):
        try:
            if self.stockrecords.num_allocated is None:
                return self.stockrecords.num_in_stock
            else:
                return self.stockrecords.num_in_stock - self.stockrecords.num_allocated
        except:
            return 0


from oscar.apps.catalogue.models import *  # noqa isort:skip
