from django import forms

from oscar.core.loading import get_model


class ShippingRuleForm(forms.ModelForm):



    class Meta:
        model = get_model('shipping', 'ShippingRule')
        fields = ['partner', 'type', 'name',  'description', 'charge_incl_tax', 'free_shipping_threshold']
