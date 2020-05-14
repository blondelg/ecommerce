import pandas as pd
from oscar.core.loading import get_model
from django.utils import timezone
from datetime import timedelta, date

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


Order = get_model('order', 'Order')


class chart_ca_histo(BaseLineChartView):

    """ get CA sum per day to build a week chart """

    def __init__(self, partner_id=None, start_date=None, end_date=None):

        """ get settings if necessary """

        if end_date is None:
            self.end_date = timezone.now()
        else:
            self.end_date = end_date

        if start_date is None:
            self.start_date = timezone.now() - timedelta(days=7)
        else:
            self.start_date = start_date

        if partner_id is None:
            self.df = pd.DataFrame(list(Order.objects.filter(date_placed__gte=self.start_date)\
                                   .filter(date_placed__lte=self.end_date).values()))
        else:
            self.df = pd.DataFrame(list(Order.objects.filter(date_placed__gte=self.start_date)\
                                   .filter(date_placed__lte=self.end_date)\
                                   .filter(partner_id=partner_id).values()))

        # transform date to 'YYYY-MM-DD'
        self.df['str_date'] = self.df['date_placed'].apply(lambda x: x.strftime('%Y-%m-%d'))

        # remove columns
        self.df = self.df[['str_date', 'total_incl_tax']]

        self.df = self.df.groupby(['str_date'], as_index=False).sum()


    def get_labels(self):
        """Return dates as yyyy-mm-dd """
        return self.df['str_date'].tolist()

    def get_providers(self):
        """  """
        return ["Sales per day"]

    def get_data(self):
        """Return 3 datasets to plot."""
        values = self.df['total_incl_tax'].tolist()

        return [[float(e) for e in values]]


class chart_new_client_histo(BaseLineChartView):

    """ get CA sum per day to build a week chart """

    def __init__(self, partner_id=None, start_date=None, end_date=None):

        """ get settings if necessary """

        if end_date is None:
            self.end_date = timezone.now()
        else:
            self.end_date = end_date

        if start_date is None:
            self.start_date = timezone.now() - timedelta(days=7)
        else:
            self.start_date = start_date

        if partner_id is None:
            self.df = pd.DataFrame(list(Order.objects.filter(date_placed__gte=self.start_date)\
                                   .filter(date_placed__lte=self.end_date).values()))
        else:
            self.df = pd.DataFrame(list(Order.objects.filter(date_placed__gte=self.start_date)\
                                   .filter(date_placed__lte=self.end_date)\
                                   .filter(partner_id=partner_id).values()))

        # transform date to 'YYYY-MM-DD'
        self.df['str_date'] = self.df['date_placed'].apply(lambda x: x.strftime('%Y-%m-%d'))

        # remove columns
        self.df = self.df[['str_date', 'total_incl_tax']]

        self.df = self.df.groupby(['str_date'], as_index=False).sum()


    def get_labels(self):
        """Return dates as yyyy-mm-dd """
        return self.df['str_date'].tolist()

    def get_providers(self):
        """  """
        return ["Sales per day"]

    def get_data(self):
        """Return 3 datasets to plot."""
        values = self.df['total_incl_tax'].tolist()

        return [[float(e) for e in values]]
