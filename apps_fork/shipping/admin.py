from django.contrib import admin

from oscar.apps.shipping.admin import *  # noqa

from oscar.core.loading import get_model


class ShippingRule(admin.ModelAdmin):
    list_display = ('partner', 'name', 'charge_incl_tax', 'free_shipping_threshold')
                    
admin.site.register(get_model('shipping', 'ShippingRule'), ShippingRule)
