from django import forms
from django.db import models

from board.forms import Form, ModelForm
from haystack.forms import ModelSearchForm

from pin.models import Pin, Resource
from board.models import Board

class PinForm(ModelForm):
    """Pin creation and edition form."""
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PinForm, self).__init__(*args, **kwargs)
        self.fields['board'].empty_label = None
        # take only user's boards
        self.fields['board'].queryset = Board.objects.filter(user=self.user)

    class Meta:
        model = Pin
        fields = ('board', 'description')


class UploadPinForm(Form):
    """Pin resource upload form."""
    file = forms.ImageField(required=True)



class DownloadPinForm(Form):
    """Pin Resource download form."""
    # image url
    src = forms.URLField(widget=forms.HiddenInput(), required=False)
    # image source page url
    url = forms.URLField(widget=forms.HiddenInput())
    # image description
    description = forms.CharField(widget=forms.HiddenInput(),
            required=False)



class RePinForm(Form):
    """Pin repinning form."""
    pin = forms.IntegerField(widget=forms.HiddenInput())

    def clean_pin(self):
        # return pin object corresponding to pin id
        # or raise an error
        pin_id = self.cleaned_data['pin']
        try:
            pin = Pin._default_manager.get(id=pin_id)
        except Pin.DoesNotExist:
            raise forms.ValidationError(
                "Invalid pin"
            )
        return pin



class PinUrlForm(Form):
    """Pin origin url form."""
    # do not use URLField because it add a trailing '/' introducing bugs.
    url = forms.CharField(widget=forms.URLInput(attrs={
        'required': 'required',
        'placeholder': 'http://'
    }))



class PinSearchForm(ModelSearchForm):
    """Pin search form."""

    def get_models(self):
        return [models.get_model('pin.pin')]



