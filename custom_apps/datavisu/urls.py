from .views import datavisu
from django.apps import apps
from django.urls import include, path



urlpatterns = [
 path('', datavisu, name='datavisu'),
]
