from django import forms

from board.models import Board, Pin



class Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.label_suffix=''



class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.label_suffix=''



class BoardForm(ModelForm):
    """Board creation and edition form."""
    class Meta:
        model = Board



class PinForm(ModelForm):
    """Pin creation and edition form."""
    class Meta:
        model = Pin
