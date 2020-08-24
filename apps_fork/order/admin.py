from django.contrib import admin
from oscar.core.loading import get_model
from oscar.apps.order.admin import *  # noqa

Donation = get_model('order', 'Donation')

class DonationAdmin(admin.ModelAdmin):
    model = Donation
    list_display = ('project', 'asso_name', 'order', 'amount')
    
admin.site.register(Donation, DonationAdmin)
