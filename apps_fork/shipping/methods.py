from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D
from decimal import *
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class MultiMethod(methods.FixedPrice):

    name = _('Multi Method')
    exponent = D('0.00')

    def __init__(self, selected_method, basket):
        rate = D(settings.OSCAR_DEFAULT_TAX_RATE)
        exponent = D('0.00')

        # declare variables as dict
        self.charge_incl_tax = {}
        self.charge_excl_tax = {}
        self.tax = {}

        # init totals
        self.charge_incl_tax['total'] = D('0.00')
        self.charge_excl_tax['total'] = D('0.00')
        self.tax['total'] = D('0.00')

        for partner in selected_method.keys():
            if basket.total_incl_tax[partner] > selected_method[partner].free_shipping_threshold:
                self.charge_incl_tax[partner] = D('0.00')
                self.charge_excl_tax[partner] = D('0.00')
                self.tax[partner] = D('0.00')
            else:
                self.charge_incl_tax[partner] = selected_method[partner].charge_incl_tax
                self.charge_excl_tax[partner] = self.charge_incl_tax[partner]/(1 + rate)
                self.tax[partner] = (self.charge_excl_tax[partner] * rate).quantize(exponent, rounding=ROUND_UP)

                # update totals
                self.charge_incl_tax['total'] += self.charge_incl_tax[partner]
                self.charge_excl_tax['total'] += self.charge_excl_tax[partner]
                self.tax['total'] += self.tax[partner]


    def calculate(self, basket, partner):
        return prices.Price(
            currency=basket.currency,
            excl_tax=self.charge_excl_tax[partner],
            incl_tax=self.charge_incl_tax[partner])

    @property
    def is_tax_known(self):
        return True

class MainMethod(methods.FixedPrice):
    code = 'main-method'
    name = _('Main Method')
    exponent = D('0.00')

    def __init__(self, shipping_rule_list, basket):
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
