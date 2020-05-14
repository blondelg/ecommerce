from apps_fork.dashboard.views import chart_ca_histo_json
from django.urls import path


urlpatterns = [
  path('chartJSON', chart_ca_histo_json, name='chart_ca_histo_json'),
]
