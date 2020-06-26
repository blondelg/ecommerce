from oscar.apps.checkout.forms import ShippingMethodForm as CoreShippingMethodForm
from django import forms



class ShippingMethodForm(CoreShippingMethodForm):


    def __init__(self, *args, **kwargs):

        extra = kwargs.pop('extra')
        super(ShippingMethodForm, self).__init__(*args, **kwargs)
        self.fields['method_code'].required = False

        i=0
        for partner, method_list in extra.items():
            self.fields[f'method_partner_name_{i}'] = forms.CharField(label='partner name', max_length=100, required = False)
            self.fields[f'method_partner_id_{i}'] = forms.IntegerField(label='partner_id', initial = int(partner.id))
            CHOICES = [(m.id, ", ".join([m.name, m.description,  str(m.charge_incl_tax) + " €"])) for m in method_list]
            self.fields[f'selected_method_{partner.id}'] = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label = "radio", required = True)
            i += 1

    def clean(self):
        return "toto"
