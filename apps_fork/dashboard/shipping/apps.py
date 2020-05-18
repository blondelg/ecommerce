from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class

class ShippingDashboardConfig(OscarDashboardConfig):
    label = 'shipping_dashboard'
    name = 'apps_fork.dashboard.shipping'
    verbose_name = _('Shipping dashboard')

    default_permissions = ['is_staff']

    def ready(self):
        self.shipping_rule_list_view = get_class(
            'dashboard.shipping.views', 'ShippingRuleListView')

        self.shipping_rule_create_view = get_class(
            'dashboard.shipping.views', 'ShippingRuleCreateView')
        self.weight_method_edit_view = get_class(
            'dashboard.shipping.views', 'WeightBasedUpdateView')
        self.weight_method_delete_view = get_class(
            'dashboard.shipping.views', 'WeightBasedDeleteView')
        # This doubles as the weight_band create view
        self.shipping_rule_detail_view = get_class(
            'dashboard.shipping.views', 'ShippingRuleDetailView')
        self.weight_band_edit_view = get_class(
            'dashboard.shipping.views', 'WeightBandUpdateView')
        self.weight_band_delete_view = get_class(
            'dashboard.shipping.views', 'WeightBandDeleteView')

    def get_urls(self):
        urlpatterns = [
            url(r'^shipping-rule/$', self.shipping_rule_list_view.as_view(),
                name='shipping-method-list'),
            url(r'^shipping-rule/create/$',
                self.shipping_rule_create_view.as_view(),
                name='shipping-method-create'),
            url(r'^shipping-rule/(?P<pk>\d+)/$',
                self.shipping_rule_detail_view.as_view(),
                name='shipping-method-detail'),
            url(r'^weight-based/(?P<pk>\d+)/edit/$',
                self.weight_method_edit_view.as_view(),
                name='shipping-method-edit'),
            url(r'^weight-based/(?P<pk>\d+)/delete/$',
                self.weight_method_delete_view.as_view(),
                name='shipping-method-delete'),
            url(r'^weight-based/(?P<method_pk>\d+)/bands/(?P<pk>\d+)/$',
                self.weight_band_edit_view.as_view(),
                name='shipping-method-band-edit'),
            url(r'^weight-based/(?P<method_pk>\d+)/bands/(?P<pk>\d+)/delete/$',
                self.weight_band_delete_view.as_view(),
                name='shipping-method-band-delete'),
        ]
        return self.post_process_urls(urlpatterns)
