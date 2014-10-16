from django import template
from django.core.urlresolvers import reverse_lazy

register = template.Library()

@register.filter
def get_paginate_url(resolver_match, page_number):
    """Take request.resolver_match object, and page number,
    return url corresponding to view with page number and other kwargs."""
    url = resolver_match.url_name
    kwargs = resolver_match.kwargs
    args = resolver_match.args
    try:
        page_number = int(page_number)
    except:
        page_number = False
    kwargs.pop('page', None)
    if page_number:
        kwargs['page'] = page_number
    
    return reverse_lazy(url, args=args, kwargs=kwargs)




