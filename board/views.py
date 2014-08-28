from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from user.models import User
from board.models import Board, Pin
from board.forms import BoardForm, PinForm


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
        self.user = User.objects.get(slug=self.kwargs['user'])
        self.board = Board .objects.get(slug=self.kwargs['board'], user=self.user)
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


class AjaxableResponseMixin(object):
    """Mixin to add ajax support to a form
    must be used with a object-based FormViem (e.g. CreateView)."""
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            html = render_to_string(self.get_template_names(),
                    self.get_context_data(form=form, request=self.request))
            return self.render_to_json_response({'form': html})
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = { 'pk': self.object.pk }
            return self.render_to_json_response(data)
        else:
            return response




class CreateBoard(CreateView, AjaxableResponseMixin):
    """View to create a new board."""
    form_class = BoardForm
    model = Board
    template_name = 'board/board_forms.html'

    def get_success_url(self):
        return reverse_lazy('boards_list',
                kwargs={'user': self.request.user.slug})

    def get_context_data(self, **kwargs):
        context = super(CreateBoard, self).get_context_data(**kwargs)
        context['title'] = 'Create a board'
        context['button'] = 'Create board'

        return context

    def form_valid(self, form):
        """If form is valid, save associated model."""
        self.object = form.save(commit=False)
        # definition of user
        self.object.user = self.request.user
        # save form
        self.object.save()
        # redirect to success url
        return redirect(self.get_success_url())



class UpdateBoard(UpdateView, AjaxableResponseMixin):
    """View to update a board."""
    pass



class DeleteBoard(DeleteView, AjaxableResponseMixin):
    """View to delete a board."""
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



