from oscar.core import prices


class OrderTotalCalculator(object):
    """
    Calculator class for calculating the order total.
    """

    def __init__(self, request=None):
        # We store a reference to the request as the total may
        # depend on the user or the other checkout data in the session.
        # Further, it is very likely that it will as shipping method
        # always changes the order total.
        self.request = request

    def calculate(self, basket, shipping_method, **kwargs):

        if basket.is_multi_partner:
            return_dict = {}
            for partner_id in basket.partner_list:
                excl_tax = basket.total_excl_tax[partner_id] + shipping_method.sub_method[partner_id].charge_excl_tax
                if basket.is_tax_known and shipping_method.is_tax_known:
                    incl_tax = basket.total_incl_tax[partner_id] + shipping_method.sub_method[partner_id].charge_incl_tax
                else:
                    incl_tax = None
                return_dict[partner_id] = prices.Price(
                    currency=basket.currency,
                    excl_tax=excl_tax, incl_tax=incl_tax)

            # calculate for parent
            excl_tax = basket.total_excl_tax['parent'] + shipping_method.excl_tax
            if basket.is_tax_known and shipping_method.is_tax_known:
                incl_tax = basket.total_incl_tax['parent'] + shipping_method.incl_tax
            else:
                incl_tax = None
            return_dict['parent'] = prices.Price(
                currency=basket.currency,
                excl_tax=excl_tax, incl_tax=incl_tax)

            return return_dict

        else:
            excl_tax = basket.total_excl_tax + shipping_method.excl_tax
            if basket.is_tax_known and shipping_method.is_tax_known:
                incl_tax = basket.total_incl_tax + shipping_method.incl_tax
            else:
                incl_tax = None
            return prices.Price(
                currency=basket.currency,
                excl_tax=excl_tax, incl_tax=incl_tax)
