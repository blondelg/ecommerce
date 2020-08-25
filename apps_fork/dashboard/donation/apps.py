from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class



class DonationDashboardConfig(OscarDashboardConfig):
    label = 'donation_dashboard'
    name = 'apps_fork.dashboard.donation'
    verbose_name = _('Donation dashboard')
    
    default_permissions = ['is_staff']
    
    permissions_map = _map = {
        'donation-list': (['is_staff'], ['partner.dashboard_access']),
    }
    
    def ready(self):
        self.donation_list_view = get_class(
            'dashboard.donation.views', 'DonationListView')
        self.donation_project_view = get_class(
            'dashboard.donation.views', 'DonationProjectsView')
            
    def get_urls(self):
        urlpatterns = [
            url(r'^donation/list$', self.donation_list_view.as_view(),
                name='donation-list'),
            url(r'^donation/projects$', self.donation_project_view.as_view(),
                name='donation-project'),
        ]
        return self.post_process_urls(urlpatterns)
