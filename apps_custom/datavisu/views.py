#from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
import pandas as pd
from django.db import models
from oscar.core.loading import get_model

# Create your views here.
#@user_passes_test(lambda u: u.is_superuser)
def datavisu(request):
    from apps_fork.analytics.models import ProductView
    # X = [1, 2, 3, 4, 5]
    # Y = [1, 2, 3, 4, 5]
    # plot = figure(title = "test")
    # plot.line(X, Y, line_width = 2)
    # script, div = components(plot)

    # Get data
    qs = ProductView.objects.all()
    df = qs.to_dataframe()

    df['date'] = df['date_created'].dt.normalize()
    df['nb'] = 1
    df = df[['date', 'nb']]
    df = df.groupby(['date']).agg(['sum'])

    p = figure(x_axis_type="datetime", title="Total product view per day", plot_height=350, plot_width=800)
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Nb product view'
    p.line(df.index.tolist(), df['nb']['sum'].tolist(),line_width = 2)

    script, div = components(p)

    return render(request, 'simple_dashboard.html', {'script': script, 'div': div})
