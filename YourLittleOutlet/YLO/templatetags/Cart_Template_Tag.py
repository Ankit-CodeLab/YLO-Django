from django import template
from YLO.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, Ordered=False)
        if qs.exists():
            return qs[0].Items.count()
    return 0

@register.filter
def split_string(value, delimiter=","):
    return value.split(delimiter)