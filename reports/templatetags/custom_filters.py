from django import template

register = template.Library()

@register.filter
def percentage(first, second):
    if second == 0:
        return 0.00
    if first is None:
        return 0.00
    return round((first / second) * 100, 2)