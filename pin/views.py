import os

from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView, TemplateView, \
        FormView
from django.views.generic.base import ContextMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlquote_plus
from django.utils.encoding import iri_to_uri
from django.contrib.auth.decorators import login_required
from django.core.files.images import ImageFile

from haystack.query import SearchQuerySet
from haystack.views import SearchView

from pinpict.settings import MEDIA_URL, MEDIA_ROOT, MAX_PIN_PER_PAGE
from board.views import AjaxableResponseMixin
from user.models import User, Notification
from pin.models import Pin, Resource, ResourceFactory
from board.models import Board
from pin.forms import PinForm, UploadPinForm, PinUrlForm, DownloadPinForm,\
        RePinForm
from pin.utils import get_sha1_hexdigest, scan_html_for_picts



class ListPinsMixin(ContextMixin):
    """Mixin to get common context for list pin views."""
    def get_context_data(self, **kwargs):
        context = super(ListPinsMixin, self).get_context_data(**kwargs)

        # for pagination links max and min
        if 'page' in self.kwargs:
            page = int(self.kwargs['page'])
            context['slice'] = "{}:{}".format(page - 4, page + 3)
        
        return context


class ListBoardPins(ListView, ListPinsMixin):
    """List all pins of a board."""
    model = Pin
    context_object_name = 'pins'
    template_name = 'pin/pin_board_list.html'
    paginate_by = MAX_PIN_PER_PAGE

    def get_queryset(self):
        self.user = get_object_or_404(User, slug=self.kwargs['user'])
        self.board = get_object_or_404(Board, slug=self.kwargs['board'],
                user=self.user)
        # add session variable to store last visited board
        self.request.session['last_visited_board'] = self.board.pk
        # if board is private and user is not board owner or staff member,
        # or allowed to read board
        # raise 404
        if (self.board.policy == 0 and self.request.user.is_authenticated()
            and self.board.user != self.request.user and not self.request.user.is_staff
            and not self.request.user in self.board.users_can_read.all() ):
            raise Http404
        return self.board.get_sorted_pins()


    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response, using the `response_class` for this
        view, with a template rendered with the given context.
        If any keyword arguments are provided, they will be
        passed to the constructor of the response class.
        """
        if self.board.policy == 0 and not self.request.user.is_authenticated():
            # if board is private and user isn't logged in, redirect to login page
            return redirect(reverse_lazy('user_login'))
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )


    def get_context_data(self, **kwargs):
        context = super(ListBoardPins, self).get_context_data(**kwargs)
        context['board'] = self.board
        context['owner'] = self.user
        
        return context



class ListUserPins(ListView, ListPinsMixin):
    """List all pins of a user."""
    model = Pin
    context_object_name = 'pins'
    template_name = 'pin/pin_user_list.html'
    paginate_by = MAX_PIN_PER_PAGE

    def get_queryset(self):
        self.user = get_object_or_404(User, slug=self.kwargs['user'])
        if self.request.user == self.user or self.request.user.is_staff:
            return self.user.pin_user.all().order_by('-date_created')
        return self.user.pin_user.filter(policy=1).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(ListUserPins, self).get_context_data(**kwargs)
        context['owner'] = self.user

        return context



class ListLastPins(ListView, ListPinsMixin):
    """List last created pins."""
    model = Pin
    context_object_name = 'pins'
    template_name = 'pin/pin_list.html'
    paginate_by = MAX_PIN_PER_PAGE

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pin.objects.all().order_by('-date_created')
        return Pin.objects.filter(policy=1).order_by('-date_created')



class ListPinLikers(ListView, ListPinsMixin):
    """List all likers of a pin."""
    model = User
    context_object_name = 'users'
    template_name = 'pin/pin_likers_list.html'
    paginate_by = 100


    def get_queryset(self):
        self.pin = get_object_or_404(Pin, pk=self.kwargs['pk'])
        return self.pin.likes.all()



class PinView(DetailView):
    """View for a specific pin."""
    model = Pin
    context_object_name = 'pin'
    template_name = 'pin/pin_view.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.board.policy == 0 
            and self.object.board.user != self.request.user 
            and not self.request.user.is_staff and 
            not self.request.user in self.object.board.users_can_read.all() ):
                raise Http404

        context = self.get_context_data(object=self.object)
        # get more like this items
        mlt_search = SearchQuerySet().more_like_this(self.object)[:20]
        pk_list = [int(item.pk) for item in mlt_search]
        mlt = Pin.objects.filter(pk__in=pk_list)
        context['mlt'] = mlt
        
        # get prev and next links
        board_pins = list(self.object.board.get_sorted_pins().values_list('id'))
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
def rate_pin(request, pk, rate):
    """View to rate a pin."""
    if not request.is_ajax():
        raise Http404
    pin = get_object_or_404(Pin, pk=pk)
    if pin.pin_user != request.user:
        raise Http404
    pin.owner_rate = int(rate)
    pin.save()
    return render(request,
            'pin/pin_rate.html',
            {'pin': pin})


@login_required
def set_main_cover(request, pk):
    """Set given pin as cover for board."""
    if not request.is_ajax():
        raise Http404
    pin = get_object_or_404(Pin, pk=pk)
    if pin.pin_user != request.user:
        raise Http404

    # get main(s) pin(s) 
    mains = pin.board.pin_set.all().filter(main=True)
    # unset main(s) pin(s)
    for main in mains:
        main.main = False
        main.save()

    pin.main = True
    pin.save()

    return HttpResponse('')


@login_required
def create_pin(request):
    """View to create a pin."""



    # from invalid pin_pict js button, redirect to find
    if (request.method == 'POST' and 'url' in request.POST
            and not 'src' in request.POST):
        print('js button')
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
            pin_form = PinForm(user=request.user)
            pin_form.initial = {}
            if request.session.get('last_visited_board'):
                pk = request.session['last_visited_board']
                pin_form.initial['board'] = pk
                board = Board.objects.get(pk=pk)
                pin_form.initial['description'] = board.pin_default_description
            if 'description' in form.cleaned_data and form.cleaned_data['description']:
                pin_form.initial['description'] = form.cleaned_data['description']

            # search user's pins with this resource
            pins = request.user.pin_user.filter(resource__source_file_url=form.cleaned_data['src'])
            # get boards using this resource
            boards = set([pin.board.title for pin in pins])
            
            return render(request, 'pin/pin_create.html', {
                'form': pin_form,
                'src': form.cleaned_data['src'],
                'submit': 'Pin it',
                'boards': boards,
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
            if pin.pin_user != request.user:
                request.session['pin_create_added_via'] = pin.pk

            pin_form = PinForm(user=request.user)
            pin_form.initial = {}
            pin_form.initial['description'] = pin.description
            if request.session.get('last_visited_board'):
                pin_form.initial['board'] = request.session['last_visited_board']

            # search user's pins with this resource
            pins = request.user.pin_user.filter(resource=pin.resource)
            # get board using this resource
            boards = set([pin.board.title for pin in pins])

            return render(request, 'pin/pin_create.html', {
                'form': pin_form,
                'resource': pin.resource,
                'submit': 'Pin it',
                'boards': boards,
            })
    
    ## final post to create the pin itself
    if request.method == 'POST':
        form = PinForm(request.POST, user=request.user)
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
                pin.added_via = Pin.objects.get(
                        pk = request.session['pin_create_added_via']
                )
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
                    print(resource)
                    print('error: make resource from url didn\'t return a resource.')
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
                print('resource error')
                return False
            
            # save pin in db
            pin.save()
            
            # send notification
            for user in pin.board.followers.all():
                if (pin.board.policy == 0 and not
                    user in pin.board.users_can_read.all()):
                    continue

                Notification.objects.create(
                    type="ADD_PIN",
                    sender=pin.pin_user,
                    receiver=user,
                    title="added a new pin on board",
                    content_object=pin
                )

            # send notification to user if it's added via another pin
            if pin.added_via:
                Notification.objects.create(
                    type="RE_PINNED",
                    sender=request.user,
                    receiver=pin.added_via.pin_user,
                    title="pinned your ",
                    content_object=pin
                )

            # redirect to board
            return redirect(reverse_lazy('board_view',
                kwargs={
                    'user': request.user.slug,
                    'board': pin.board.slug
                }))

    else:        
        form = PinForm(user=request.user)
        form.initial = {}
        if request.session.get('last_visited_board'):
            pk = request.session['last_visited_board']
            form.initial['board'] = pk
            board = Board.objects.get(pk=pk)
            form.initial['description'] = board.pin_default_description


    boards = None
    ## request arrive from upload pin with new uploaded file
    if request.session.get('pin_create_tmp_resource'):
        src = MEDIA_URL + request.session['pin_create_tmp_resource']
    ## request arrive from upload pin with no uploaded file (it exists)
    elif request.session.get('pin_create_resource'):
        try:
            resource = Resource.objects.get(
                pk = request.session['pin_create_resource']
            )
        except:
            raise Http404
        src = MEDIA_URL + 'previews/236/' + resource.previews_path
        # search user's pins with this resource
        pins = request.user.pin_user.filter(resource=resource)
        # get board using this resource
        boards = set([pin.board.title for pin in pins])
    ## pin arrives from find_pin or pin button
    elif request.session.get('pin_create_src'):
        src = request.session['pin_create_src']
        # search user's pins with this resource
        pins = request.user.pin_user.filter(resource__source_file_url=src)
        # get boards using this resource
        boards = set([pin.board.title for pin in pins])

    ## request is error
    else:
        # here should be some invalid form (no board in select or no description) handler !!!
        raise Http404

    return render(request, 'pin/pin_create.html', {
        'form': form,
        'src': src,
        'submit': 'Pin it',
        'boards': boards,
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
        Handles GET requests and instantiates a blank version of the form.
        """
        self.object = self.get_object()
        # ensure user is pin's owner
        self.check_user()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(self.get_context_data(form=form))


    def get_form_kwargs(self):
        """
        Returns the keyword arguments for intantiating the form.
        """

        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'user': self.request.user,
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


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

class UserSearchView(SearchView):
    """To filter a search with a given user."""
    def build_form(self, form_kwargs=None):
        print(self.searchqueryset)
        from pprint import pprint
        pprint(self.searchqueryset[0].__dict__)
        self.searchqueryset = self.searchqueryset.filter(user=self.request.user.username)
        print(self.searchqueryset)

        return super(UserSearchView, self).build_form(form_kwargs)


