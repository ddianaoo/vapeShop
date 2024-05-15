from django import template
from ..models import STATUS_CHOICES

register = template.Library()

@register.filter
def display_status(status):
    return STATUS_CHOICES[int(status)][1] or 'Unknown'

@register.filter
def calculate_order_total(order_details):
    total_price = sum(detail.quantity * detail.product.price for detail in order_details)
    return total_price
