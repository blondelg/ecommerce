from decimal import Decimal as D
from decimal import *
from django.conf import settings
from oscar.apps.partner.strategy import Selector as CoreSelector
from oscar.apps.partner.strategy import UseFirstStockRecord as CoreUseFirstStockRecord
from oscar.apps.partner.strategy import StockRequired as CoreStockRequired
from oscar.apps.partner.strategy import FixedRateTax as CoreFixedRateTax
from oscar.apps.partner.strategy import Structured as CoreStructured
from oscar.apps.partner.strategy import FixedRateTax as CoreFixedRateTax
from oscar.core.loading import get_class


TaxInclusiveFixedPrice = get_class('partner.prices', 'TaxInclusiveFixedPrice')


class Selector(CoreSelector):
    def strategy(self, request=None, user=None, **kwargs):
        return Tautoko(request)


class FixedRateTax(CoreFixedRateTax):
    """
    Pricing policy mixin for use with the ``Structured`` base strategy.  This
    mixin applies a fixed rate tax to the base price from the product's
    stockrecord.  The price_incl_tax is quantized to two decimal places.
    Rounding behaviour is Decimal's default
    """
    rate = D('0.00')  # Subclass and specify the correct rate
    exponent = D('0.00')  # Default to two decimal places

    def pricing_policy(self, product, stockrecord):
        if not stockrecord or stockrecord.price_excl_tax is None:
            return UnavailablePrice()
        rate = self.get_rate(product, stockrecord)
        exponent = self.get_exponent(stockrecord)
        tax = (stockrecord.price_excl_tax * rate).quantize(exponent, rounding=ROUND_UP)

        return TaxInclusiveFixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price_excl_tax,
            tax=tax)

    def parent_pricing_policy(self, product, children_stock):
        stockrecords = [x[1] for x in children_stock if x[1] is not None]
        if not stockrecords:
            return UnavailablePrice()

        # We take price from first record
        stockrecord = stockrecords[0]
        rate = self.get_rate(product, stockrecord)
        exponent = self.get_exponent(stockrecord)
        tax = (stockrecord.price_excl_tax * rate).quantize(exponent, rounding=ROUND_UP)

        return TaxInclusiveFixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price_excl_tax,
            tax=tax)

    def get_rate(self, product, stockrecord):
        """
        This method serves as hook to be able to plug in support for varying tax rates
        based on the product.

        TODO: Needs tests.
        """
        return self.rate

    def get_exponent(self, stockrecord):
        """
        This method serves as hook to be able to plug in support for a varying exponent
        based on the currency.

        TODO: Needs tests.
        """
        return self.exponent


class Tautoko(CoreUseFirstStockRecord, CoreStockRequired, FixedRateTax, CoreStructured):

    rate = D(settings.OSCAR_DEFAULT_TAX_RATE)
