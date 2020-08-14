from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name= 'get_val')
def get_val(dict, key):
    return dict.get(key)