from django import forms

from board.forms import Form, ModelForm

from pin.models import Pin, Resource


class PinForm(ModelForm):
    """Pin creation and edition form."""
    class Meta:
        model = Pin
        fields = ('board', 'description', 'source')



class UploadPinForm(ModelForm):
    """Pin file upload form."""
    class Meta:
        model = Resource
        fields = ('source_file',)
