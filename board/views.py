import json

from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from pinpict.settings import MEDIA_URL
from user.models import User
from board.models import Board
from board.forms import BoardForm, UpdateBoardForm
from notification.models import Notification

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
        if not self.request.user.is_authenticated():
            return context
        # get owner's private boards 
        privates = Board.privates.filter(user=self.user)
        if self.user == self.request.user or self.request.user.is_staff:
            context['private_boards'] = privates
            return context
        allowed = privates.filter(users_can_read=self.request.user)
        if allowed:
            context['private_boards'] = allowed

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

    def auto_follow(self):
        """Automatically add owner's followers to this board."""
        for user in self.object.user.followers.all():
            self.object.add_follower(user, notification=False)
            
    def send_notifications(self):
        """Send notifications to all suscribed
        users who have rights on board."""
        for user in self.object.user.followers.all():
            if (self.object.policy == 0 and 
                not user in self.object.users_can_read.all()):
                continue

            Notification.objects.create(
                sender=self.object.user,
                receiver=user,
                title="created a new board",
                content_object=self.object
            )

    def form_valid(self, form):
        """If form is valid, save associated model."""
        self.object = form.save(commit=False)
        # definition of user
        self.object.user = self.request.user
        # definition of policy
        self.set_policy()
        # save form
        self.object.save()
        # send notifications
        self.send_notifications()
        # add followers to board
        self.auto_follow()
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


@login_required
def boardFollow(request, pk):
    """Add a follower to a board."""
    if not request.is_ajax():
        raise Http404
    board = get_object_or_404(Board, id=pk)
    board.add_follower(request.user)

    return HttpResponse(reverse_lazy('board_unfollow',
            kwargs={'pk': pk}))


@login_required
def boardUnfollow(request, pk):
    """Remove a follower from a board."""
    if not request.is_ajax():
        raise Http404
    board = get_object_or_404(Board, id=pk)
    board.remove_follower(request.user)

    return HttpResponse(reverse_lazy('board_follow',
            kwargs={'pk': pk}))



def getCoversList(request, pk):
    """Returns a json list of all pins id of the given board."""
    board = get_object_or_404(Board, id=pk)
    data = board.pin_set.all().select_related('resource').values('pk', 'resource__previews_path')
    to_dump = [{'pk': item['pk'], 'previews_path': "{}previews/216-160/{}".format(
        MEDIA_URL, item['resource__previews_path'])} for item in data]

    return JsonResponse(to_dump, safe=False)
