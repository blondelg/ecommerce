from django.apps import apps
from django.conf.urls import include, url
from django.utils.translation import gettext_lazy as _

from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class
from oscar.apps.dashboard.apps import DashboardConfig as CoreDashboardConfig


class DashboardConfig(CoreDashboardConfig):
    label = 'dashboard'
    name = 'apps_fork.dashboard'
    
    def ready(self):

        self.donation_app = apps.get_app_config('donation_dashboard')
        super().ready()
        
        
    def get_urls(self):
        from django.contrib.auth import views as auth_views
        from django.contrib.auth.forms import AuthenticationForm
        
        urls = [url(r'^donations/', include(self.donation_app.urls[0]))]
        post_process_urls = super().get_urls()
        post_process_urls += self.post_process_urls(urls)
        
        return post_process_urls
        

