from django import template
register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.filter(name='sort_url')
def sort_url(url, order):
    new_url = '/'.join(url.split('/')[:-2]) + f'/{order}'

    return new_url
