from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct


class Product(AbstractProduct):

    @property
    def stock_level(self):
        return self.stockrecords.values()[0]['num_in_stock'] - self.stockrecords.values()[0]['num_allocated']


from oscar.apps.catalogue.models import *  # noqa isort:skip
