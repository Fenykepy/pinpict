from rest_framework import generics
from rest_framework import permissions

from user.models import User
from user.serializers import *



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


