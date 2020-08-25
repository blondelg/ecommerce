from django import template

register = template.Library()

@register.filter(name='percent')
def percent(value):
    """returns percentage"""
    return round(value * 100, 2)
    
@register.filter(name='percent_no_digit')
def percent_no_digit(value):
    """returns percentage"""
    return round(value * 100)
