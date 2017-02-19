from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes

from pinpict.permissions import IsStaffOrAuthenticatedAndCreateOnly, \
        IsBoardAllowed, IsStaffOrReadOnly

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
    permission_classes = ( IsBoardAllowed, IsStaffOrReadOnly,)

    def get_serializer_class(self):
        user = get_object_or_404(User, slug=self.kwargs['user'])
        if self.request.user == user or self.request.user.is_staff:
            return BoardSerializer
        else:
            return PublicBoardSerializer

    def get_object(self):
        user = get_object_or_404(User, slug=self.kwargs['user'])
        return Board.objects.get(user=user,slug=self.kwargs['board'])



@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def user_public_boards_list(request, user, format=None):
    """
    Returns a list of a user's publics boards without pagination.
    """
    user = get_object_or_404(User, slug=user)
    boards = Board.publics.filter(user=user).only(
        'title', 'slug', 'n_pins', 'policy', 'user')
    serializer = BoardAbstractSerializer(boards, many=True)

    return Response(serializer.data)



@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def user_private_boards_list(request, user, format=None):
    """
    This view presents a list of a member's privates boards :
        - all private boards if user is owner;
        - all private boards if user is admin;
        - allowed private boards if user is authenticated;
    """
    user = get_object_or_404(User, slug=user)
    # return all private boards if user is owner or staff
    if request.user == user or request.user.is_staff:
        queryset = Board.privates.filter(user=user)
    else:
        queryset = Board.privates.filter(
                user=user,
                users_can_read=request.user
        )
        
    boards = queryset.only(
        'title', 'slug', 'n_pins', 'policy', 'user')
    serializer = BoardAbstractSerializer(boards, many=True)

    return Response(serializer.data)

