from django.contrib import admin
from django.contrib import admin
from oscar.core.loading import get_model
from oscar.apps.order.admin import *  # noqa

ContentProjet = get_model('content', 'ContentProjet')

class ContentProjetAdmin(admin.ModelAdmin):
    model = ContentProjet
    list_display = ('target', 'asso', 'achievement', 'achievement_percent', 'achieved', 'donation_count')
    
admin.site.register(ContentProjet, ContentProjetAdmin)

