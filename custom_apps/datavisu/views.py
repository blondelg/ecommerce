from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components

# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
def datavisu(request):
    X = [1, 2, 3, 4, 5]
    Y = [1, 2, 3, 4, 5]
    plot = figure(title = "test")
    plot.line(X, Y, line_width = 2)
    script, div = components(plot)
    return render(request, 'simple_dashboard.html', {'script': script, 'div': div})
