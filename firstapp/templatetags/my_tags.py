from django import template

register = template.Library()


@register.filter(name="mod")
def mod(num, val):
    return num % val == 1
