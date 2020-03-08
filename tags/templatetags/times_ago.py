from django import template

from tags.helpers import pretty_date

register = template.Library()


@register.filter(name='times_ago')
def times_ago(datetime_obj):
    return pretty_date(datetime_obj)
