from django import template

from ..models import Book

register = template.Library()


@register.inclusion_tag('calibre/genres.html', takes_context=True)
def genres(context, root=None, prefix=''):
    if prefix:
        prefix += '.'
    context.update({'genres': root or Book.get_genres(context.get('user')),
                    'prefix': prefix})
    return context


@register.filter
def last(value, delimiter='.'):
    return value.split(delimiter)[-1]
