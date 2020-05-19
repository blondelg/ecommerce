from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D
from decimal import *
from django.conf import settings

class MainMethod(methods.FixedPrice):
    # code = 'standard'
    # name = 'Standard shipping'
    # charge_incl_tax = D('5.00')
    exponent = D('0.00')

    def __init__(self, shipping_rule, basket):
        rate = D(settings.OSCAR_DEFAULT_TAX_RATE)
        exponent = D('0.00')

        # check if partner sub-total incl tax
        # is greater than threshold
        if basket.total_incl_tax[shipping_rule.partner] < shipping_rule.free_shipping_threshold:
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

class Standard(methods.FixedPrice):
    code = 'standard'
    name = 'Standard shipping'
    charge_incl_tax = D('5.00')
    exponent = D('0.00')

    def __init__(self, charge_excl_tax=None, charge_incl_tax=None):
        rate = D(settings.OSCAR_DEFAULT_TAX_RATE)
        exponent = D('0.00')
        if charge_incl_tax is not None:
            self.charge_incl_tax = charge_incl_tax

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

class Express(methods.FixedPrice):
    code = 'express'
    name = 'Express shipping'
    charge_excl_tax = D('10.00')

    def __init__(self, charge_excl_tax=None, charge_incl_tax=None):
        if charge_excl_tax is not None:
            self.charge_excl_tax = charge_excl_tax
        if charge_incl_tax is not None:
            self.charge_incl_tax = charge_incl_tax

    def calculate(self, basket):
        return prices.Price(
            currency=basket.currency,
            excl_tax=self.charge_excl_tax,
            incl_tax=self.charge_incl_tax)

    @property
    def is_tax_known(self):
        return True
