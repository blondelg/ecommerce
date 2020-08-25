from django.views import generic
from django.shortcuts import render
from django.conf import settings
import pandas as pd

from oscar.core.loading import get_class, get_model
from oscar.views.generic import BulkEditMixin



Donation = get_model('order', 'Donation')
Project = get_model('content', 'ContentProjet')


class DonationListView(BulkEditMixin, generic.ListView):
    model = Donation
    template_name = "oscar/dashboard/donation/donation_list.html"
    context_object_name = "donations"
    paginate_by = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE

    def get_queryset(self):
        if self.request.user.is_staff:
            return Donation.objects.get_queryset().order_by('-pk')

        
    def get_paginate_by(self, queryset):
        return self.paginate_by
        
        
class DonationProjectsView(BulkEditMixin, generic.ListView):
    model = Project
    template_name = "oscar/dashboard/donation/donation_projects.html"
    context_object_name = "projects"
    paginate_by = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.get_queryset().order_by('-achievement_percent')
        
    def get_paginate_by(self, queryset):
        return self.paginate_by


