from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from user.models import User
from user.serializers import *


@api_view(('GET', ))
@permission_classes([AllowAny])
def user_root(request, format=None):
    return Response({
        'token-obtain': reverse('token-obtain', request=request, format=format),
        'token-refresh': reverse('token-refresh', request=request, format=format),
        'current-user': reverse('current-user', request=request, format=format),
        'user-list': reverse('user-list', request=request, format=format),
    })


class CurrentUserDetail(generics.RetrieveUpdateAPIView):
    """
    This view presents request's user and allows to update it.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = SafeUserSerializer

    def get_object(self):
        return self.request.user



class PublicUserDetail(generics.RetrieveAPIView):
    """
    This view presents a user public's datas.
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = PublicUserSerializer
    queryset = User.objects.all()
    lookup_field = 'slug'


class UserList(generics.ListCreateAPIView):
    """
    This view presents a list of all users and allows
    new users to be created.
    """
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'slug'



class UserDetail(generics.RetrieveUpdateAPIView):
    """
    This view presents a specific user and allows
    to update or delete it.
    """
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'slug'




