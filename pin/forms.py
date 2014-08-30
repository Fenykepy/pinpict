from django import forms

from board.forms import Form, ModelForm

from pin.models import Pin


class PinForm(ModelForm):
    """Pin creation and edition form."""
    class Meta:
        model = Pin
        fields = ('board', 'description', 'source')



class UploadPinForm(Form):
    """Pin file upload form."""
    file = forms.ImageField(widget=forms.FileInput(attrs={
        'required': 'required'
    }), required=True, label='')
