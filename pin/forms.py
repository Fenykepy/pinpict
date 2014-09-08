from django import forms

from board.forms import Form, ModelForm

from pin.models import Pin, Resource


class PinForm(ModelForm):
    """Pin creation and edition form."""
    class Meta:
        model = Pin
        fields = ('board', 'description')



class UploadPinForm(ModelForm):
    """Pin resource upload form."""
    class Meta:
        model = Resource
        fields = ('source_file',)



class DownloadPinForm(Form):
    """Pin Resource download form."""
    # image url
    href = forms.HiddenInput()
    # image source page url
    url = forms.HiddenInput()
    # image alt
    alt = forms.HiddenInput()



class PinUrlForm(Form):
    """Pin origin url form."""
    # do not use URLField because it add a trailing '/' introducing bugs.
    url = forms.CharField(widget=forms.URLInput(attrs={'required': 'required'}))



