from oscar.apps.checkout.forms import ShippingMethodForm as CoreShippingMethodForm
from django import forms



class ShippingMethodForm(CoreShippingMethodForm):

    method_name = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):


        methods = kwargs.pop('methods', [])
        methods = list(methods.values())[0]
        super().__init__(*args, **kwargs)
        self.fields['method_name'].choices = ((m.name, m.name) for m in methods)
        for m in methods:
            print(m)
            print(dir(m))
