from django import forms
from django.utils.translation import gettext_lazy as _

class UploadTypeSelectForm(forms.Form):
    """
    Form to get upload type
    """
    OPTIONS = (
    ("Catalogue", "Catalogue"),
    ("Stock", "Stock"),
    )


    type = forms.CharField(
    label='Type d\'upload',
    widget=forms.Select(choices=OPTIONS))
