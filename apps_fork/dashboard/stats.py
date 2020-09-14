import pandas as pd
from oscar.core.loading import get_model
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Q

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from chartjs.views.columns import BaseColumnsHighChartsView


Order = get_model('order', 'Order')
Line = get_model('order', 'Line')
Partner = get_model('partner', 'Partner')

def get_partner_id(user):
    """ from a given user returns partner_id id exists """
    try:
        return Partner.objects.get(users=user).pk
    except:
        return None


class chart_best_sellers(BaseLineChartView):

    """ bar chart that displays all sells per products """

    def retrieve_data(self):

        self.partner_id = get_partner_id(self.__dict__['request'].user)
        if self.partner_id is None:
            self.df = pd.DataFrame(list(Line.objects.all().values()))
        else:
            self.df = pd.DataFrame(list(Line.objects.filter(partner_id=self.partner_id).values()))

        # subset columns
        self.df = self.df[['title', 'quantity']]

        # group by title
        self.df = self.df.groupby(['title'], as_index=False).sum()

        self.title = "toto en vacance"
        self.yUnit = "cm"

    def get_labels(self):
        """Return product titles """
        self.retrieve_data()
        return self.df['title'].tolist()

    def get_data(self):
        """ get data from database """
        return [self.df['quantity'].tolist()]

    def get_providers(self):
        """   """
        return ["Total item sold"]



class chart_ca_histo(BaseLineChartView):

    """ get CA sum per day to build a week chart """

    def retrieve_data(self, start_date=None, end_date=None):

        self.partner_id = get_partner_id(self.__dict__['request'].user)

        if end_date is None:
            self.end_date = timezone.now()
        else:
            self.end_date = end_date

        if start_date is None:
            self.start_date = timezone.now() - timedelta(days=7)
        else:
            self.start_date = start_date

        if self.partner_id is None:
            self.df = pd.DataFrame(list(Order.objects.filter(date_placed__gte=self.start_date)\
                                   .filter(date_placed__lte=self.end_date).values()))
        else:
            self.df = pd.DataFrame(list(Order.objects.filter(date_placed__gte=self.start_date)\
                                   .filter(date_placed__lte=self.end_date)\
                                   .filter(partner_id=self.partner_id).values()))

        core_df = pd.date_range(self.start_date, periods=7, freq='D').to_frame(name="date_placed", index=False)
        core_df['total_incl_tax'] = 0
        self.df = pd.concat([self.df, core_df])

        # transform date to 'YYYY-MM-DD'
        self.df['str_date'] = self.df['date_placed'].apply(lambda x: x.strftime('%Y-%m-%d'))

        # remove columns
        self.df = self.df[['str_date', 'total_incl_tax']]

        self.df = self.df.groupby(['str_date'], as_index=False).sum()

    def get_dataset_options(self, index, color):
        opt = {
            "backgroundColor": "rgba(1, 1, 1, 0)",
            "borderColor": "rgba(%d, %d, %d, 1)",
            "pointBackgroundColor": "rgba(%d, %d, %d, 1)",
            "pointBorderColor": "#fff",
            "fill": "false",
        }
        return opt

    def get_labels(self):
        """Return dates as yyyy-mm-dd """
        self.retrieve_data()
        return self.df['str_date'].tolist()

    def get_providers(self):
        """  """
        return ["Sales per day"]

    def get_data(self):
        """Return 3 datasets to plot."""
        values = self.df['total_incl_tax'].tolist()

        return [[float(e) for e in values]]



class chart_new_client_histo(BaseLineChartView):

    """ get new client sum per day to build a week chart """

    def retrieve_data(self, start_date=None, end_date=None):

        self.partner_id = get_partner_id(self.__dict__['request'].user)

        if end_date is None:
            self.end_date = timezone.now()
        else:
            self.end_date = end_date

        if start_date is None:
            self.start_date = timezone.now() - timedelta(days=7)
        else:
            self.start_date = start_date

        if self.partner_id is None:
            self.df = pd.DataFrame(list(Order.objects\
                                        .filter(~Q(structure='child'))\
                                        .filter(date_placed__gte=self.start_date)\
                                        .filter(date_placed__lte=self.end_date).values()))
        else:
            self.df = pd.DataFrame(list(Order.objects\
                                        .filter(~Q(structure='parent'))\
                                        .filter(date_placed__gte=self.start_date)\
                                        .filter(date_placed__lte=self.end_date)\
                                        .filter(partner_id=self.partner_id).values()))


        #add missing dates
        core_df = pd.date_range(self.start_date, periods=7, freq='D').to_frame(name="date_placed", index=False)
        core_df['date_placed'] = core_df['date_placed'].dt.date
        core_df['user_id'] = 0
        self.df = pd.concat([self.df, core_df])

        # transform date to 'YYYY-MM-DD'
        self.df['date'] = self.df['date_placed']
        print(self.df)

        # remove columns
        self.df = self.df[['date', 'user_id']]

        #self.df = self.df.groupby(['user_id'], as_index=False).min()
        self.df = self.df.groupby(['date'], as_index=False).count()
        self.df = self.df.groupby(['date'], as_index=False).sum()

        # convert date to str
        self.df['str_date'] = self.df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        self.df = self.df[['str_date', 'user_id']]


    def get_dataset_options(self, index, color):
        opt = {
            "backgroundColor": "rgba(1, 1, 1, 0)",
            "borderColor": "rgba(%d, %d, %d, 1)",
            "pointBackgroundColor": "rgba(%d, %d, %d, 1)",
            "pointBorderColor": "#fff",
            "fill": "false",
        }
        return opt

    def get_labels(self):
        """Return dates as yyyy-mm-dd """
        self.retrieve_data()
        return self.df['str_date'].tolist()

    def get_providers(self):
        """  """
        return ["New clients per day"]

    def get_data(self):
        """Return 3 datasets to plot."""
        values = self.df['user_id'].tolist()

        return [[float(e) for e in values]]
