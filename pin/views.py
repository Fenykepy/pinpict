import os

from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView, TemplateView, \
        FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from board.views import AjaxableResponseMixin
from user.models import User
from pin.models import Pin, Resource
from board.models import Board
from pin.forms import PinForm, UploadPinForm
from pin.utils import get_sha1_hexdigest, generate_previews


class ListPins(ListView):
    """List all pins of a board."""
    model = Pin
    context_object_name = 'pins'
    template_name = 'pin/pin_list.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, slug=self.kwargs['user'])
        self.board = get_object_or_404(Board, slug=self.kwargs['board'], user=self.user)
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




class ChoosePinOrigin(TemplateView, AjaxableResponseMixin):
    """View to choose origin of a pin (computer or web)."""
    template_name = 'pin/pin_choose_origin.html'



class CreatePin(CreateView, AjaxableResponseMixin):
    """View to create a pin."""
    pass



class UpdatePin(UpdateView, AjaxableResponseMixin):
    """View to update a pin."""
    pass



class DeletePin(DeleteView, AjaxableResponseMixin):
    """View to delete a pin."""
    pass



class UploadPin(CreateView, AjaxableResponseMixin):
    """View to upload a pin file."""
    model = Resource
    template_name = 'board/board_forms.html'
    form_class = UploadPinForm
    success_url = reverse_lazy('create_pin')

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
            print('clone')
            return redirect(self.get_success_url() + '?resource={0}'.format(clone[0].pk))

        self.object.width = self.object.source_file.width
        self.object.height = self.object.source_file.height
        self.object.size = self.object.source_file.size
        basename, ext = os.path.splitext(self.object.source_file.name)
        self.object.type = ext.lower().lstrip('.')

        # save object
        self.object.save()

        # create previews
        generate_previews(self.object)




        # redirect to create_pin view
        return redirect(self.get_success_url() + '?resource={0}'.format(self.object.pk))



class ChoosePinUrl(FormView, AjaxableResponseMixin):
    """View to choose pin origin url."""
    pass



class FindPin(ListView):
    """View to choose image to pin from given url."""
    pass
