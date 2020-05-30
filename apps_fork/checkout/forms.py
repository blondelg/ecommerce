from oscar.apps.checkout.forms import ShippingMethodForm as CoreShippingMethodForm
from django import forms



class ShippingMethodForm(CoreShippingMethodForm):

    method_partner = forms.CharField(label='partner', max_length=100)
    method_name = forms.CharField(label='method name', max_length=100)
    method_is_selected = forms.BooleanField(required=False)

    # def __init__(self, *args, **kwargs):
    #
    #
    #     methods = kwargs.pop('methods', [])
    #     methods = list(methods.values())[0]
    #     super().__init__(*args, **kwargs)
    #     self.fields['method_name'].choices = ((m.name, m.name) for m in methods)
