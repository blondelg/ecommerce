from django.db import models
from oscar.apps.partner.abstract_models import AbstractStockRecord
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from decimal import Decimal as D



class StockRecord(AbstractStockRecord):

    product = models.OneToOneField(
        'catalogue.Product',
        on_delete=models.CASCADE,
        related_name="stockrecords",
        verbose_name=_("Product"))

    def save(self, *args, **kwargs):
        try:
            tax_rate = D(settings.OSCAR_DEFAULT_TAX_RATE)
            self.price_excl_tax = self.price_retail / (1 + tax_rate)
        except Exception as e:
            self.price_excl_tax = self.price_retail

        super(StockRecord, self).save(*args, **kwargs)

from oscar.apps.partner.models import *  # noqa isort:skip
