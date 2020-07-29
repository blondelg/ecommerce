from oscar.apps.checkout.mixins import OrderPlacementMixin as CoreOrderPlacementMixin
from oscar.core.loading import get_class, get_model


OrderCreator = get_class('order.utils', 'OrderCreator')
order = get_model('order', 'Order')
donation = get_model('order', 'Donation')


class OrderPlacementMixin(CoreOrderPlacementMixin):

    """ class surcharge to integrate donation accountability """

    def place_order(self, order_number, user, basket, shipping_address,
                    shipping_method, shipping_charge, order_total,
                    billing_address=None, **kwargs):
        """
        Writes the order out to the DB including the payment models
        """
        # Create saved shipping address instance from passed in unsaved
        # instance
        shipping_address = self.create_shipping_address(user, shipping_address)

        # We pass the kwargs as they often include the billing address form
        # which will be needed to save a billing address.
        billing_address = self.create_billing_address(
            user, billing_address, shipping_address, **kwargs)

        if 'status' not in kwargs:
            status = self.get_initial_order_status(basket)
        else:
            status = kwargs.pop('status')

        if 'request' not in kwargs:
            request = getattr(self, 'request', None)
        else:
            request = kwargs.pop('request')

        order = OrderCreator().place_order(
            user=user,
            order_number=order_number,
            basket=basket,
            shipping_address=shipping_address,
            shipping_method=shipping_method,
            shipping_charge=shipping_charge,
            total=order_total,
            billing_address=billing_address,
            status=status,
            request=request,
            **kwargs)
        self.save_payment_details(order)
        self.register_donation(basket, kwargs, order_number)
        return order
    
    
    
    def register_donation(self, basket, order_kwargs, order_number):
        """ register donation when successful """
        current_order = order.objects.get(number=order_number)
        new_record = donation(project=order_kwargs['project'], order=current_order, amount=order_kwargs['donation'])
        new_record.save()
