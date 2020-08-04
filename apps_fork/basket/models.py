from decimal import Decimal as D
from django.db import models
from oscar.apps.basket.abstract_models import AbstractBasket
from oscar.apps.basket.abstract_models import AbstractLine
from oscar.core.loading import get_model

partner = get_model('partner', 'Partner')
projet = get_model('content', 'ContentProjet')

class Basket(AbstractBasket):

    project = models.ForeignKey(projet, on_delete=models.SET_NULL, null=True)
    
    def _get_total(self, property, partner_id=None):
        """
        For executing a named method on each line of the basket
        and returning the total.
        """
        if partner_id is None:
            total = D('0.00')
            for line in self.all_lines():
                try:
                    total += getattr(line, property)
                # except ObjectDoesNotExist:
                #     # Handle situation where the product may have been deleted
                #     pass
                except TypeError:
                    # Handle Unavailable products with no known price
                    info = self.get_stock_info(line.product, line.attributes.all())
                    if info.availability.is_available_to_buy:
                        raise
                    pass
            return total
        else:
            total = D('0.00')
            for line in self.partner_lines(partner_id):
                try:
                    total += getattr(line, property)
                except ObjectDoesNotExist:
                    # Handle situation where the product may have been deleted
                    pass
                except TypeError:
                    # Handle Unavailable products with no known price
                    info = self.get_stock_info(line.product, line.attributes.all())
                    if info.availability.is_available_to_buy:
                        raise
                    pass
            return total


    def partner_lines(self, partner_id):
        """ return lines according to a given parner id """
        return self.all_lines().filter(product__partner_id=partner_id)
        
    def set_project(self, project_id):
        """ Set a project from project id """
        self.project = projet.objects.get(pk=project_id)
        self.save()

    @property
    def is_multi_partner(self):
        # Return true if there is several partners on this order
        partners = {}
        for line in self.all_lines():
            partners[line.partner] = 1
        if len(partners.keys()) > 1:
            return True
        else:
            return False

    @property
    def partner_list(self):
        # Return a list with partners ids
        partners = []
        for line in self.all_lines():
            partners.append(line.partner)

        return list(set(partners))

    @property
    def partners(self):
        # Return a list with partners
        return [partner.objects.filter(id=p_id) for p_id in self.partner_list()]


    @property
    def total_excl_tax(self):
        # Return total line price excluding tax per partner
        if self.is_multi_partner:
            total = {}
            for partner in self.partner_list:
                total[partner] = self._get_total('line_price_excl_tax_incl_discounts', partner)

            total['parent'] = self._get_total('line_price_excl_tax_incl_discounts')

            return total
        else:
            return self._get_total('line_price_excl_tax_incl_discounts')

    @property
    def total_excl_tax_all(self):
        # return total for mix and non mix basket
        return self._get_total('line_price_excl_tax_incl_discounts')


    @property
    def total_incl_tax(self):
        # Return total price inclusive of tax and discounts per partner
        if self.is_multi_partner:
            total = {}
            for partner in self.partner_list:
                total[partner] = self._get_total('line_price_incl_tax_incl_discounts', partner)

            total['parent'] = self._get_total('line_price_incl_tax_incl_discounts')

            return total
        else:
            return self._get_total('line_price_incl_tax_incl_discounts')

    @property
    def total_incl_tax_all(self):
        # Return total for mix and non mix baskets
        return self._get_total('line_price_incl_tax_incl_discounts')


class Line(AbstractLine):

    @property
    def partner(self):
        return self.product.partner



from oscar.apps.basket.models import *  # noqa isort:skip
