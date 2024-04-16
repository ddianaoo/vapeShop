from django import template

register = template.Library()

@register.filter
def display_status(status, choices):
    return choices[int(status)][1] or 'Unknown'
