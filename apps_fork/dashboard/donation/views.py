from django.views import generic
from django.shortcuts import render
import pandas as pd

from oscar.core.loading import get_class, get_model



Donation = get_model('order', 'Donation')


class DonationListView(generic.ListView):
    model = Donation
    template_name = "oscar/dashboard/donation/donation_list.html"
    context_object_name = "donations"

    def get_queryset(self):

        if self.request.user.is_staff:
            return [Donation.objects.all(), Donation.objects.all()]
            
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Authors'
        return data
        
    def get_project_progress(self):
        """ for each project, calculates sum of donations """
        pass



