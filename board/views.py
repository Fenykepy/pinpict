from django.views.generic import ListView, DetailView
from django.views.generic.base import ContextMixin

from user.models import User
from board.models import Board, Pin, Pin_board


class ListBoards(ListView):
    """List all boards for one user."""
    model = Board
    context_object_name= 'boards'
    template_name = 'board/board_list.html'

    def get_queryset(self):
        user = User.objects.get(slug=self.kwargs['user'])
        return user.board_set.all()

class ListPins(ListView):
    """List all pins of a board."""
    model = Pin
    context_object_name = 'pins'
    template_name = 'board/pin_list.html'

    def get_queryset(self):
        user = User.objects.get(slug=self.kwargs['user'])
        board = Board .objects.get(slug=self.kwargs['board'], user=user)
        return board.pins.all()

class PinView(DetailView):
    pass

