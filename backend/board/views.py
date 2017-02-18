from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from board.serializers import *
from board.models import Board


@api_view(('GET', ))
def board_root(request, format=None):
    return Response({
        'boards-list': reverse('boards-list', request=request, format=format),
    })

class BoardsList(generics.ListCreateAPIView):
    """
    This view presents a list of all boards and allows new
    boards to be created.
    """
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = BoardSerializer
    queryset = Board.objects.all()




