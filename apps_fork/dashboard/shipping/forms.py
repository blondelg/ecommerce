from django import forms

from oscar.core.loading import get_model


class ShippingRuleForm(forms.ModelForm):


    class Meta:
        model = get_model('shipping', 'ShippingRule')
        fields = ['partner', 'name',  'description', 'charge_incl_tax', 'free_shipping_threshold']

    def __init__(self, *args, **kwargs):
        super(ShippingRuleForm, self).__init__(*args, **kwargs)
        print("DEBUG KWARGS")
        print(kwargs)
        try:
            assert kwargs['initial']['partner'] is None

        except:
            self.fields['partner'].widget = forms.HiddenInput()
