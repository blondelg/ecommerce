from django.apps import apps
from django.urls import include, path, re_path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls


#if settings.DEBUG:
import debug_toolbar

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include(apps.get_app_config('oscar').urls[0])),

    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),

    re_path(r'blog/', include(wagtail_urls)),

    path('__debug__/', include(debug_toolbar.urls)),

    # Optional URL for including your own vanilla Django urls/views
    #re_path(r'', include('myapp.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    #re_path(r'', include(wagtail_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
