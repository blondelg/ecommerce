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
            
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['df'] = self.get_project_progress().to_html(justify='left', index=False, classes='table table-striped table-bordered')
            return data
        except:
            pass
        
    def get_project_progress(self):
        """ for each project, calculates sum of donations """
        
        # get data
        donations = Donation.objects.all()
        projects = Project.objects.all()

        # queryset to dataframe
        df_donations = pd.DataFrame(list(donations.values()))
        df_projects = pd.DataFrame(list(projects.values()))[['title', 'target']]
        
        # left join
        df = df_donations.merge(df_projects, how='left', left_on='project_name', right_on='title')[['project_name', 'asso_name', 'target', 'amount']]
        
        # calculate sums
        df = df.groupby(by=['project_name', 'asso_name', 'target'], axis=0, as_index=False).sum()
        
        # calculate progress
        df['progress'] = df.apply(lambda x: (x['amount'] / x['target']) * 100, axis=1)
        
        # rename headers
        df.columns = ['Project', 'Association', 'Target', 'Total', 'Progress']
        
        # update columns formats
        df['Target'] = df['Target'].apply(lambda x: str(x) + " €")
        df['Total'] = df['Total'].apply(lambda x: str(x) + " €")
        df['Progress'] = df['Progress'].apply(lambda x: str(round(x, 2)) + " %")

        
        return df
        
    def get_paginate_by(self, queryset):
        return self.paginate_by


