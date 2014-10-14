import os

from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView, TemplateView, \
        FormView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlquote_plus
from django.utils.encoding import iri_to_uri
from django.contrib.auth.decorators import login_required
from django.core.files.images import ImageFile

from pinpict.settings import MEDIA_URL, MEDIA_ROOT
from board.views import AjaxableResponseMixin
from user.models import User
from pin.models import Pin, Resource, ResourceFactory
from board.models import Board
from pin.forms import PinForm, UploadPinForm, PinUrlForm, DownloadPinForm,\
        RePinForm
from pin.utils import get_sha1_hexdigest, scan_html_for_picts




class ListBoardPins(ListView):
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
        context = super(ListBoardPins, self).get_context_data(**kwargs)
        context['board'] = self.board
        context['owner'] = self.user

        return context



class ListUserPins(ListView):
    """List all pins of a user."""
    model = Pin
    context_object_name = 'pins'
    template_name = 'pin/pin_user_list.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, slug=self.kwargs['user'])

        return self.user.pin_user.filter(policy=1).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(ListUserPins, self).get_context_data(**kwargs)
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
        # get prev and next links
        board_pins = list(self.object.board.pin_set.values_list('id'))
        index = board_pins.index((self.object.id,))
        length = len(board_pins)

        if index == 0:
            context['prev'] = False
        else:
            context['prev'] = board_pins[index - 1][0]
        
        next = index + 1
        if next == length:
            context['next'] = False
        else:
            context['next'] = board_pins[next][0]

        return self.render_to_response(context)



class ChoosePinOrigin(TemplateView, AjaxableResponseMixin):
    """View to choose origin of a pin (computer or web)."""
    template_name = 'pin/pin_choose_origin.html'



@login_required
def create_pin(request):
    """View to create a pin."""

    # from invalid pin_pict js button, redirect to find
    if (request.method == 'POST' and 'url' in request.POST
            and not 'src' in request.POST):
        form = DownloadPinForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            return redirect(reverse_lazy('find_pin') + '?url={}'.format(
            urlquote_plus(url)))



    # form arrive from pin_pict js button, or pin_find
    if (request.method == 'POST' and 'url' in request.POST
            and 'src' in request.POST):
        form = DownloadPinForm(request.POST)
        if form.is_valid():
            # set session variables
            request.session['pin_create_source'] = form.cleaned_data['url']
            request.session['pin_create_src'] = form.cleaned_data['src']
            pin_form = PinForm()
            pin_form.fields["board"].queryset = Board.objects.filter(user=request.user)
            pin_form.initial = {}
            if 'description' in form.cleaned_data:
                pin_form.initial['description'] = form.cleaned_data['description']
            if request.session.get('last_visited_board'):
                pin_form.initial['board'] = request.session['last_visited_board']


            return render(request, 'pin/pin_create.html', {
                'form': pin_form,
                'src': form.cleaned_data['src'],
                'submit': 'Pin it',
            })

    # form arrive from existing pin's pin it button
    if request.method == 'POST' and 'pin' in request.POST:
        form = RePinForm(request.POST)
        if form.is_valid():
            # set pin object
            pin = form.cleaned_data['pin']
            # set session variables
            request.session['pin_create_resource'] = pin.resource.pk
            request.session['pin_create_source'] = pin.source
            if pin.pin_user and pin.pin_user != request.user:
                request.session['pin_create_added_via'] = pin.pin_user.pk

            pin_form = PinForm()
            pin_form.fields["board"].queryset = Board.objects.filter(user=request.user)
            pin_form.initial = {}
            pin_form.initial['description'] = pin.description
            if request.session.get('last_visited_board'):
                pin_form.initial['board'] = request.session['last_visited_board']

            return render(request, 'pin/pin_create.html', {
                'form': pin_form,
                'resource': pin.resource,
                'submit': 'Pin it',
            })
    
    ## final post to create the pin itself
    if request.method == 'POST':
        form = PinForm(request.POST)
        if form.is_valid():
            pin = form.save(commit=False)

            # if posted board doesn't belong to user raise 404
            if pin.board.user != request.user:
                raise Http404
            # set pin user
            pin.pin_user = request.user
            # set pin policy
            pin.policy = pin.board.policy
            # set added_via if any
            if request.session.get('pin_create_added_via'):
                added_via = User.objects.get(
                        pk = request.session['pin_create_added_via']
                )
                pin.added_via = added_via
                del request.session['pin_create_added_via']
            # set source
            if request.session.get('pin_create_source'):
                pin.source = request.session['pin_create_source'][:2000]
                del request.session['pin_create_source']
            # set resource
            if request.session.get('pin_create_resource'):
                # if resource in session (repin or clone on upload)
                resource = get_object_or_404(Resource,
                        pk = request.session['pin_create_resource']
                )
                pin.resource = resource
                del request.session['pin_create_resource']
            elif request.session.get('pin_create_src'):
                # if resource has to be downloaded
                fact = ResourceFactory()
                resource = fact.make_resource_from_url(
                        request.session['pin_create_src'],
                        request.user,
                )
                if resource:
                    pin.resource = resource
                else:
                    #print('error: make resource from url didn\'t return a resource.')
                    return False
                del request.session['pin_create_src']
            elif request.session.get('pin_create_tmp_resource'):
                # if resource is a temporary file
                tmp_path = os.path.join(MEDIA_ROOT, request.session['pin_create_tmp_resource'])
                fact = ResourceFactory()
                resource = fact.make_resource_from_file(tmp_path, request.user)
                if resource:
                    pin.resource = resource
                # delete old tmp file
                os.remove(tmp_path)

                del request.session['pin_create_tmp_resource']
            else:
                # raise an resource error
                return False
            
            # save pin in db
            pin.save()

            # redirect to board
            return redirect(reverse_lazy('board_view',
                kwargs={
                    'user': request.user.slug,
                    'board': pin.board.slug
                }))

    else:        
        form = PinForm()
        form.fields["board"].queryset = Board.objects.filter(user=request.user)
        form.initial = {}
        if request.session.get('last_visited_board'):
            form.initial['board'] = request.session['last_visited_board']



    ## request arrive from upload pin with new uploaded file
    if request.session.get('pin_create_tmp_resource'):
        print(request.session['pin_create_tmp_resource'])
        src = MEDIA_URL + request.session['pin_create_tmp_resource']
    ## request arrive from upload pin with no uploaded file (it exists)
    elif request.session.get('pin_create_resource'):
        resource = Resource.objects.get(
            pk = request.session['pin_create_resource']
        )
        src = MEDIA_URL + 'previews/236/' + resource.previews_path
    ## pin arrives from find_pin or pin button
    elif request.session.get('pin_create_src'):
        src = request.session['pin_create_src']

    ## request is error
    else:
        # here should be some invalid form (no board in select or no description) handler !!!
        raise Http404

    return render(request, 'pin/pin_create.html', {
        'form': form,
        'src': src,
        'submit': 'Pin it',
    })




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
        self.board = self.object.board
        self.object.delete()

        return redirect(self.get_success_url())


    # ensure that user is pin's owner !!!
    def get_success_url(self):
        return reverse_lazy('board_view',
                kwargs={
                    'user': self.request.user.slug,
                    'board': self.board.slug,
                })



class UploadPin(FormView, AjaxableResponseMixin):
    """View to upload a pin resource."""
    template_name = 'board/board_forms.html'
    form_class = UploadPinForm

    def get_context_data(self, **kwargs):
        context = super(UploadPin, self).get_context_data(**kwargs)
        context['title'] = 'Upload an image'
        context['button'] = 'Updload'

        return context


    def form_valid(self, form):
        """If form is valid, save associated model."""
        file = form.cleaned_data['file']
        fact = ResourceFactory()
        resource = fact.make_tmp_resource(file)
        # if resource is a Resource object (get a clone)
        if resource and isinstance(resource, Resource):
            # add resource ID to session
            self.request.session['pin_create_resource'] = resource.pk
            # redirect to create pin view
            return redirect(reverse_lazy('create_pin'))
        # if resource is a string (url relative to MEDIA_URL)
        if resource and isinstance(resource, str):
            # add file path to session
            self.request.session['pin_create_tmp_resource'] = resource
        # redirect to create_pin view
        return redirect(reverse_lazy('create_pin'))



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
        #print('url received in form: {}'.format(url))
        return redirect(reverse_lazy('find_pin') + '?url={}'.format(
            urlquote_plus(url)))



class FindPin(TemplateView):
    """View to choose image to pin from given url."""
    template_name = 'pin/pin_find.html'

    def get(self, request, *args, **kwargs):
        # it seems that django automaticaly decode arguments.
        # for safety, encode non ascii char if any
        self.url = iri_to_uri(self.request.GET.get('url', ''))
        #print('url after iri_to_uri by find pin: {}'.format(self.url))
        # if url is not an absolute url
        if self.url[:4] != 'http':
            raise Http404        

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(FindPin, self).get_context_data(**kwargs)
        context['picts'] = scan_html_for_picts(self.url)
        context['url'] = self.url
        context['form'] = DownloadPinForm()


        return context


