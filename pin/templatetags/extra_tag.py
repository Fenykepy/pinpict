from django import template
from django.core.urlresolvers import reverse_lazy

register = template.Library()

@register.filter
def get_paginate_url(request, page_number):
    """Take request object, and page number,
    return url corresponding to view with page number, args, other kwargs
    and query string."""
    url = request.resolver_match.url_name
    kwargs = request.resolver_match.kwargs
    args = request.resolver_match.args
    query_string = request.META.get('QUERY_STRING')
    if query_string:
        query_string = '?' + query_string
    try:
        page_number = int(page_number)
    except:
        page_number = False
    kwargs.pop('page', None)
    if page_number:
        kwargs['page'] = page_number
    
    return reverse_lazy(url, args=args, kwargs=kwargs) + query_string




