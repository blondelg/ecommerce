from apps_fork.dashboard.views import chart_ca_histo_json
from apps_fork.dashboard.views import chart_new_client_histo_json
from django.urls import path


urlpatterns = [
  path('chart_ca_JSON', chart_ca_histo_json, name='chart_ca_histo_json'),
  path('chart_newclient_JSON', chart_new_client_histo_json, name='chart_new_client_histo_json'),

]
