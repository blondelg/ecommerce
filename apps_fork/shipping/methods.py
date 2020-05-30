from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D
from decimal import *
from django.conf import settings

class MainMethod(methods.FixedPrice):
    # code = 'standard'

    # charge_incl_tax = D('5.00')
    exponent = D('0.00')

    def __init__(self, shipping_rule, basket):
        rate = D(settings.OSCAR_DEFAULT_TAX_RATE)
        exponent = D('0.00')
        self.name = shipping_rule.name
        self.description = shipping_rule.description

        # check if partner sub-total incl tax
        # is greater than threshold
        if basket.total_incl_tax[shipping_rule.partner] > shipping_rule.free_shipping_threshold:
            self.charge_incl_tax = D('0.00')
        else:
            self.charge_incl_tax = shipping_rule.charge_incl_tax

        self.charge_excl_tax = self.charge_incl_tax/(1 + rate)
        self.tax = (self.charge_excl_tax * rate).quantize(exponent, rounding=ROUND_UP)


    def calculate(self, basket):
        return prices.Price(
            currency=basket.currency,
            excl_tax=self.charge_excl_tax,
            incl_tax=self.charge_incl_tax)

    @property
    def is_tax_known(self):
        return True

class Free(methods.FixedPrice):
    """
    This shipping method specifies that shipping is free.
    """
    # code = 'free-shipping'
    # name = _('Free shipping')

    def calculate(self,basket):
        # If the charge is free then tax must be free (musn't it?) and so we
        # immediately set the tax to zero
        return prices.Price(
            currency=basket.currency,
            excl_tax=D('0.00'), tax=D('0.00'))
