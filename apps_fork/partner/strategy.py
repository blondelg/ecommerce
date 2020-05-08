from decimal import Decimal as D
from django.conf import settings
from oscar.apps.partner.strategy import Selector as CoreSelector
from oscar.apps.partner.strategy import UseFirstStockRecord as CoreUseFirstStockRecord
from oscar.apps.partner.strategy import StockRequired as CoreStockRequired
from oscar.apps.partner.strategy import FixedRateTax as CoreFixedRateTax
from oscar.apps.partner.strategy import Structured as CoreStructured



class Selector(CoreSelector):
    def strategy(self, request=None, user=None, **kwargs):
        return Tautoko(request)


class Tautoko(CoreUseFirstStockRecord, CoreStockRequired, CoreFixedRateTax, CoreStructured):

    rate = D(settings.OSCAR_DEFAULT_TAX_RATE)
