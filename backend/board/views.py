from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from pinpict.permissions import IsStaffOrAuthenticatedAndCreateOnly, \
        IsBoardAllowed

from board.serializers import *
from board.models import Board

from user.models import User


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
    permission_classes = (IsStaffOrAuthenticatedAndCreateOnly, )
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    # automatically add user on save
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This view presents a specific board and allows
    to update or delete it.
    """
    permission_classes = (permissions.IsAdminUser, IsBoardAllowed)

    def get_serializer_class(self):
        user = get_object_or_404(User, slug=self.kwargs['user'])
        if self.request.user == user or self.request.user.is_staff:
            return BoardSerializer
        else:
            return PublicBoardSerializer

    def get_object(self):
        user = get_object_or_404(User, slug=self.kwargs['user'])
        return Board.objects.get(user=user,slug=self.kwargs['board'])



class UserPublicBoardsList(generics.ListAPIView):
    """
    This view presents a list of a member's publics boards.
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = BoardAbstractSerializer

    def get_queryset(self):
        """Return queryset."""
        user = get_object_or_404(User, slug=self.kwargs['user'])
        return Board.publics.filter(user=user)



class UserPrivateBoardsList(generics.ListAPIView):
    """
    This view presents a list of a member's privates boards :
        - all private boards if user is owner;
        - all private boards if user is admin;
        - allowed private boards if user is authenticated;
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = BoardAbstractSerializer

    def get_queryset(self):
        """Return queryset."""
        user = get_object_or_404(User, slug=self.kwargs['user'])
        queryset = Board.privates.filter(user=user)
        # return all private boards
        if self.request.user == user or self.request.user.is_staff:
            return queryset
        # user is authenticated but nor owner nor staff
        else:
            return queryset.filter(users_can_read=self.request.user)


