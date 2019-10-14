from rest_framework import generics, permissions

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes

from pin.serializers import *
from pin.models import Pin, Tag


@api_view(('GET', ))
@permission_classes([permissions.IsAdminUser])
def pin_root(request, format=None):
    return Response({
        'tags-list': reverse('tags-list', request=request, format=format),
    })


@api_view(('GET', ))
def tags_flat_list(request, format=None):
    """
    Returns a flat list of all tags without pagination.
    """
    tags = Tag.objects.order_by('name').values_list('name', flat=True)

    return Response(tags)
