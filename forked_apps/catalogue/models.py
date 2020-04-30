from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct


class Product(AbstractProduct):

    @property
    def stock_level(self):
        try:
            if self.stockrecords.values()[0]['num_allocated'] is None:
                return self.stockrecords.values()[0]['num_in_stock']
            else:
                return return self.stockrecords.values()[0]['num_in_stock'] - self.stockrecords.values()[0]['num_allocated']
        except:
            return 0


from oscar.apps.catalogue.models import *  # noqa isort:skip
