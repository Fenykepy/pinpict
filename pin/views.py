from rest_framework import generics, permissions, status

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView


from pinpict.permissions import IsStaffOrAuthenticatedAndCreateOnly, \
        IsStaffOrReadOnly

from pin.serializers import *
from pin.models import Pin, Tag
from pin.utils import PicturesFinder
from board.models import Board


@api_view(('GET', ))
@permission_classes([permissions.IsAdminUser])
def pin_root(request, format=None):
    return Response({
        'pin-list': reverse('pin-list', request=request, format=format),
        'tag-list': reverse('tag-list', request=request, format=format),
        'scan-url': reverse('scan-url', request=request, format=format),
    })



@api_view(('GET', ))
def tags_flat_list(request, format=None):
    """
    Returns a flat list of all tags without pagination.
    """
    tags = Tag.objects.order_by('name').values_list('name', flat=True)

    return Response(tags)



class ScanUrl(APIView):
    """
    Returns a list of all pictures found on given url.
    """

    serializer_class = UrlSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        serializer = UrlSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data.get('url')
            full_search = serializer.validated_data.get('full_search')
            finder = PicturesFinder(url, full_search=full_search)
            # serialize results
            serializer = ScannedPictureSerializer(finder.get_results(), many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PinList(generics.ListCreateAPIView):
    """
    This view presents a list of all pins and allows new
    pins to be created.
    """
    permission_classes = (IsStaffOrAuthenticatedAndCreateOnly, )
    serializer_class = PinSerializer
    queryset = Pin.objects.all()

    def perform_create(self, serializer):
        """
        We automatically add user on save
        As different user can have a board with same slug,
        we get board filtered by request user.
        """
        board_slug = serializer.initial_data.get('board')
        board = Board.objects.get(user=self.request.user, slug=board_slug)
        serializer.save(user=self.request.user, board=board)



class PinDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This view presents a specific pin and allows
    to update or delete it.
    """
    permission_classes = ( IsStaffOrReadOnly,)
    serializer_class = PinSerializer
    queryset = Pin.objects.all()

