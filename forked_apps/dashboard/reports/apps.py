import oscar.apps.dashboard.reports.apps as apps

from oscar.core.loading import get_class
from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from custom_apps.datavisu.views import datavisu
from oscar.core.application import OscarDashboardConfig


class ReportsDashboardConfig(apps.OscarDashboardConfig):
    label = 'reports_dashboard'
    name = 'forked_apps.dashboard.reports'
    verbose_name = _('Reports dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.index_view = get_class('dashboard.reports.views', 'IndexView')
        self.datavisu_view = datavisu

    def get_urls(self):
        urls = [
            url(r'^reports$', self.index_view.as_view(), name='reports-index'),
            url(r'^datavisu$', self.datavisu_view, name='datavisu'),
        ]
        return self.post_process_urls(urls)
