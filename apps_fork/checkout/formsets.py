from django.forms import formset_factory
from apps_fork.checkout.forms import ShippingMethodForm

ShippingMethodFormSet = formset_factory(ShippingMethodForm, extra=0)
