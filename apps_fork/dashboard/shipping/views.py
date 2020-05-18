from django import shortcuts
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from oscar.core.loading import get_class, get_model

ShippingRuleForm = get_class('dashboard.shipping.forms', 'ShippingRuleForm')
ShippingRule = get_model('shipping', 'ShippingRule')



class ShippingRuleListView(generic.ListView):
    model = ShippingRule
    template_name = "oscar/dashboard/shipping/shipping_based_list.html"
    context_object_name = "methods"


class ShippingRuleCreateView(generic.CreateView):
    model = ShippingRule
    form_class = ShippingRuleForm
    template_name = "oscar/dashboard/shipping/shipping_based_form.html"

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        print(kwargs)
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_success_url(self):

        msg = render_to_string(
            'oscar/dashboard/shipping/messages/method_created.html',
            {'method': self.object})
        messages.success(self.request, msg, extra_tags='safe noicon')
        return reverse('dashboard:shipping-method-detail',
                       kwargs={'pk': self.object.pk})


class ShippingRuleDetailView(generic.CreateView):
    model = ShippingRule
    form_class = ShippingRuleForm
    template_name = "oscar/dashboard/shipping/weight_based_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.method = shortcuts.get_object_or_404(
            ShippingRule, pk=kwargs['pk'])
        return super().dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        # kwargs['method'] = self.method
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['method'] = self.method
        return ctx

    def get_success_url(self):
        msg = render_to_string(
            'oscar/dashboard/shipping/messages/band_created.html',
            {'band': self.object})
        messages.success(self.request, msg, extra_tags='safe noicon')
        return reverse('dashboard:shipping-method-detail',
                       kwargs={'pk': self.method.pk})


class ShippingRuleUpdateView(generic.UpdateView):
    model = ShippingRule
    form_class = ShippingRuleForm
    template_name = "oscar/dashboard/shipping/weight_based_form.html"
    context_object_name = "method"

    def get_success_url(self):
        msg = render_to_string(
            'oscar/dashboard/shipping/messages/method_updated.html',
            {'method': self.object})
        messages.success(self.request, msg, extra_tags='safe noicon')
        return reverse('dashboard:shipping-method-detail',
                       kwargs={'pk': self.object.pk})


class ShippingRuleDeleteView(generic.DeleteView):
    model = ShippingRule
    template_name = "oscar/dashboard/shipping/weight_band_delete.html"
    context_object_name = "band"

    def dispatch(self, request, *args, **kwargs):
        self.method = shortcuts.get_object_or_404(
            WeightBased, pk=kwargs['method_pk'])
        return super().dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        return self.method.bands.all()

    def get_success_url(self):
        msg = render_to_string(
            'oscar/dashboard/shipping/messages/band_deleted.html',
            {'band': self.object})
        messages.success(self.request, msg, extra_tags='safe noicon')
        return reverse('dashboard:shipping-method-detail',
                       kwargs={'pk': self.method.pk})


class ShippingRuleDeleteView(generic.DeleteView):
    model = ShippingRule
    template_name = "oscar/dashboard/shipping/weight_based_delete.html"
    context_object_name = "method"

    def get_success_url(self):
        msg = render_to_string(
            'oscar/dashboard/shipping/messages/method_deleted.html',
            {'method': self.object})
        messages.success(self.request, msg, extra_tags='safe noicon')
        return reverse('dashboard:shipping-method-list')
