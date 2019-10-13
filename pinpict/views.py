from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

@api_view(('GET', ))
def api_root(request, format=None):
    return Response({
        'users-menu': reverse('user-root', request=request, format=format),
        'boards-menu': reverse('board-root', request=request, format=format),
    })


