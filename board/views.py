from django.views.generic import ListView

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



