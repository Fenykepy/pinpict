import os

from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView, TemplateView, \
        FormView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlquote_plus, urlunquote_plus
from django.contrib.auth.decorators import login_required


#from pinpict.settings import LOGIN_URL !!!
from board.views import AjaxableResponseMixin
from user.models import User
from pin.models import Pin, Resource
from board.models import Board
from pin.forms import PinForm, UploadPinForm, PinUrlForm, DownloadPinForm
from pin.utils import get_sha1_hexdigest, generate_previews, \
        scan_html_for_picts


class ListPins(ListView):
    """List all pins of a board."""
    model = Pin
    context_object_name = 'pins'
    template_name = 'pin/pin_list.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, slug=self.kwargs['user'])
        self.board = get_object_or_404(Board, slug=self.kwargs['board'],
                user=self.user)
        # add session variable to store last visited board
        self.request.session['last_visited_board'] = self.board.pk
        # if board is private
        if self.board.policy == 0:
            # if user isn't logged in, redirect to login page
            if not self.request.user.is_authenticated():
                #redirect(LOGIN_URL)!!!
                raise Http404
            # if user isn't board owner, raise 404
            elif self.board.user != self.request.user:
                raise Http404
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
    template_name = 'pin/pin_view.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.board.policy == 0 
            and self.object.board.user != self.request.user):
                raise Http404


        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)





class ChoosePinOrigin(TemplateView, AjaxableResponseMixin):
    """View to choose origin of a pin (computer or web)."""
    template_name = 'pin/pin_choose_origin.html'



class CreatePin(CreateView, AjaxableResponseMixin):
    """View to create a pin."""
    form_class = PinForm
    model = Pin
    template_name = 'pin/pin_create.html'

    def dispatch(self, request, *args, **kwargs):
        print(self.request.session.get('resource'))
        # get resource from session or raise 404
        if not self.request.session.get('resource'):
            raise Http404
        self.resource = get_object_or_404(Resource, pk=self.request.session['resource'])
        return super(CreateView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(CreatePin, self).get_context_data(**kwargs)
        context['resource'] = self.resource
        context['submit'] = 'Pin it'

        return context


    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # set initial data
        form.initial = {}
        if self.request.session.get('last_visited_board'):
            form.initial['board'] = self.request.session['last_visited_board']
        if self.request.session.get('resource_description'):
            form.initial['description'] = self.request.session['resource_description']

        # ensure that only user's boards are listed
        form.fields["board"].queryset = Board.objects.filter(user=request.user)
        return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        """If form is valid, save associated model."""
        self.object = form.save(commit=False)
        
        # if posted board doesn't belongs to user raise 404
        if self.object.board.user != self.request.user:
            raise Http404
        self.object.resource = self.resource

        # if object has been downloaded
        if self.request.session.get('resource_source'):
            self.object.source = self.request.session['resource_source']
            del self.request.session['resource_source']
        # save object
        self.object.save()
        # del session variables
        del self.request.session['resource']
        if self.request.session.get('resource_description'):
            del self.request.session['resource_description']

        # redirect to board
        return redirect(reverse_lazy('board_view',
                kwargs={
                    'user': self.request.user.slug,
                    'board': self.object.board.slug
                }))





class UpdatePin(UpdateView, AjaxableResponseMixin):
    """View to update a pin."""
    form_class = PinForm
    model = Pin
    template_name = 'pin/pin_create.html'
    context_object_name = 'pin'

    def check_user(self):
        """Raise 404 if user isn't object's owner."""
        if self.object.board.user != self.request.user:
            raise Http404


    def get(self, request, *args, **kwargs):
        """
        Handles get requests and instantiates a blank version of the form.
        """
        self.object = self.get_object()
        # ensure user is pin's owner
        self.check_user()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # ensure that only user's boards are listed
        form.fields["board"].queryset = Board.objects.filter(user=request.user)
        return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        """If form is valaid, save associated model."""
        self.object = form.save(commit=False)

        # ensure user is pin's owner
        self.check_user()
        self.object.save()

        return redirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super(UpdatePin, self).get_context_data(**kwargs)
        context['submit'] = 'Save changes'
        context['delete'] = 'Delete pin'
        context['resource'] = self.object.resource

        return context


    def get_success_url(self):
        return reverse_lazy('pin_view',
                kwargs={'pk': self.object.pk})



class DeletePin(DeleteView, AjaxableResponseMixin):
    """View to delete a pin."""
    model  = Pin
    template_name = 'pin/pin_delete.html'
    context_object_name = 'pin'

    def check_user(self):
        """Raise 404 if user isn't object's owner."""
        if self.object.board.user != self.request.user:
            raise Http404


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # ensure user is pin's owner
        self.check_user()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    
    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()

        # ensure user is pin's owner
        self.check_user()
        self.object.delete()

        return redirect(self.get_success_url())


    # ensure that user is pin's owner !!!
    def get_success_url(self):
        return reverse_lazy('boards_list',
                kwargs={'user': self.request.user.slug})



class UploadPin(CreateView, AjaxableResponseMixin):
    """View to upload a pin resource."""
    model = Resource
    template_name = 'board/board_forms.html'
    form_class = UploadPinForm

    def get_context_data(self, **kwargs):
        context = super(UploadPin, self).get_context_data(**kwargs)
        context['title'] = 'Upload an image'
        context['button'] = 'Updload'

        return context


    def form_valid(self, form):
        """If form is valid, save associated model."""
        self.object = form.save(commit=False)
        # compute file sha1
        self.object.sha1 = get_sha1_hexdigest(self.object.source_file)

        # search resource with same hash
        clone = Resource.objects.filter(sha1=self.object.sha1)

        # if we have another resource with same hash
        # returns create_pin view with it's ID, and don't save anything
        if clone:
            # add resource ID to session
            self.request.session['resource'] = clone.pk
            # redirect to create pin view
            return redirect(reverse_lazy('create_pin'))

        self.object.width = self.object.source_file.width
        self.object.height = self.object.source_file.height
        self.object.size = self.object.source_file.size
        basename, ext = os.path.splitext(self.object.source_file.name)
        self.object.type = ext.lower().lstrip('.')

        # save object
        self.object.save()

        # add resource ID to session
        self.request.session['resource'] = self.object.pk

        # create previews
        generate_previews(self.object)

        # redirect to create_pin view
        return redirect(reverse_lazy('create_pin'))



@login_required
def download_pin(request):
    """View to download a pin resource from a webpage."""
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DownloadPinForm(request.POST)
        if form.is_valid():
            # add url to session
            request.session['resource_source'] = form.cleaned_data['url']
            # add alt to session
            request.session['resource_description'] = form.cleaned_data['alt']
            # create resource from href


            # add resource ID to session
            #request.session['resource'] = resource.pk
            request.session['resource'] = 1

            return redirect(reverse_lazy('create_pin'))
        else:
            # form is invalid, raise 404
            raise Http404

    else:
        # form is build in pin_find view, no get here.
        raise Http404
    



class ChoosePinUrl(FormView, AjaxableResponseMixin):
    """View to choose pin origin url."""
    form_class = PinUrlForm
    template_name = 'board/board_forms.html'

    def get_context_data(self, **kwargs):
        context = super(ChoosePinUrl, self).get_context_data(**kwargs)
        context['title'] = 'Add a pin from a website'
        context['button'] = 'Next'

        return context

    def form_valid(self, form):
        """If form is valid, redirect to find page."""
        url = form.cleaned_data['url']
        return redirect(reverse_lazy('find_pin') + '?url={}'.format(
            urlquote_plus(url)))



class FindPin(TemplateView):
    """View to choose image to pin from given url."""
    template_name = 'pin/pin_find.html'

    def get_context_data(self, **kwargs):
        url = urlunquote_plus(self.request.GET.get('url'))
        context = super(FindPin, self).get_context_data(**kwargs)
        context['picts'] = scan_html_for_picts(url)
        context['url'] = url
        context['form'] = DownloadPinForm()


        return context


