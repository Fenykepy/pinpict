from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404

from user.models import User
from board.models import Board
from board.forms import BoardForm, UpdateBoardForm


class ListBoards(ListView):
    """List all boards for one user."""
    model = Board
    context_object_name= 'boards'
    template_name = 'board/board_list.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, slug=self.kwargs['user'])
        return Board.publics.filter(user=self.user)

    def get_context_data(self, **kwargs):
        context = super(ListBoards, self).get_context_data(**kwargs)
        #context['range4'] = [i+1 for i in range(4)]
        context['owner'] = self.user
        if self.user == self.request.user:
            context['private_boards'] = Board.privates.filter(user=self.user)

        return context



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

    def set_policy(self):
        """Set policy before saving object."""
        self.object.policy = 1

    def form_valid(self, form):
        """If form is valid, save associated model."""
        self.object = form.save(commit=False)
        # definition of user
        self.object.user = self.request.user
        # definition of policy
        self.set_policy()
        # save form
        self.object.save()
        # redirect to success url
        return redirect(self.get_success_url())



class CreatePrivateBoard(CreateBoard):
    """View to create a new private board."""
    form_class = BoardForm

    def get_context_data(self, **kwargs):
        context = super(CreateBoard, self).get_context_data(**kwargs)
        context['title'] = 'Create a private board'
        context['button'] = 'Create a private board'

        return context

    def set_policy(self):
        """Set policy before saving object."""
        self.object.policy = 0



class UpdateBoard(UpdateView, AjaxableResponseMixin):
    """View to update a board."""
    form_class = UpdateBoardForm
    model = Board
    template_name = 'board/board_forms.html'

    def dispatch(self, request, *args, **kwargs):
        # if user is not board owner, 404
        if self.kwargs['user'] != request.user.slug:
            raise Http404
        return super(UpdateBoard, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('boards_list',
                kwargs={'user': self.request.user.slug})

    def get_context_data(self, **kwargs):
        context = super(UpdateBoard, self).get_context_data(**kwargs)
        context['title'] = 'Edit a board'
        context['button'] = 'Save changes'
        context['delete'] = 'Delete board'

        return context

    def get_object(self, queryset=None):
        self.user = get_object_or_404(User, slug=self.kwargs['user'])
        return get_object_or_404(Board, user=self.user, slug=self.kwargs['board'])



class DeleteBoard(DeleteView, AjaxableResponseMixin):
    """View to delete a board."""
    model = Board
    template_name = 'board/board_delete.html'
    context_object_name = 'board'


    def dispatch(self, request, *args, **kwargs):
        # if user is not board owner, 404
        if self.kwargs['user'] != request.user.slug:
            raise Http404
        return super(DeleteBoard, self).dispatch(request, *args, **kwargs)


    def get_object(self, queryset=None):
        self.user = get_object_or_404(User, slug=self.kwargs['user'])
        return get_object_or_404(Board, user=self.user, slug=self.kwargs['board'])

    def get_success_url(self):
        return reverse_lazy('boards_list',
                kwargs={'user': self.request.user.slug})



