from oscar.apps.basket.abstract_models import AbstractBasket
from oscar.apps.basket.abstract_models import AbstractLine

class Basket(AbstractBasket):

    def partner_lines(self, partner_id): # TO UPDATE ############################################################
        """ return lines according to a given parner id """
        return self.all_lines().filter(product__partner_id=partner_id)

    @property # TO UPDATE #####################################################################
    def is_multi_partner(self):
        # Return true if there is several partners on this order
        partners = {}
        print("toto")
        for line in self.all_lines():
            partners[line.partner_id] = 1
        if len(partners.keys()) > 1:
            return True
        else:
            return False

    @property # TO UPDATE ######################################################################
    def partner_list(self):
        # Return a list with partners ids
        partners = []
        for line in self.all_lines():
            partners.append(line.partner_id)

        return list(set(partners))


class Line(AbstractLine):

    @property # TO UPDATE ##############################################################################
    def partner_id(self):
        print(self.product.partner_id)
        return self.product.partner_id



from oscar.apps.basket.models import *  # noqa isort:skip
