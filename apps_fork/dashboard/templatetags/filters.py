from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def remove_blank(phrase):
    return phrase.replace(" ", "x")
