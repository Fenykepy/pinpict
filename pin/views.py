from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView

from board.views import AjaxableResponseMixin
from user.models import User
from pin.models import Pin, Resource
from board.models import Board
from pin.forms import PinForm

class ListPins(ListView):
    """List all pins of a board."""
    model = Pin
    context_object_name = 'pins'
    template_name = 'board/pin_list.html'

    def get_queryset(self):
        self.user = User.objects.get(slug=self.kwargs['user'])
        self.board = Board.objects.get(slug=self.kwargs['board'], user=self.user)
        return self.board.pin_set.all()

    def get_context_data(self, **kwargs):
        context = super(ListPins, self).get_context_data(**kwargs)
        context['board'] = self.board
        context['owner'] = self.user

        return context



class PinView(DetailView):
    """View for a specific pin."""
    model = Pin
    context_object_name = 'pin'
    template_name = 'board/pin_view.html'
    pass



class CreatePin(CreateView, AjaxableResponseMixin):
    """View to create a pin."""
    pass



class UpdatePin(UpdateView, AjaxableResponseMixin):
    """View to update a pin."""
    pass



class DeletPin(DeleteView, AjaxableResponseMixin):
    """View to delete a pin."""
    pass



