from django import template

register = template.Library()

@register.filter(name='percent')
def percent(value):
    """returns percentage"""
    return round(value * 100, 2)
