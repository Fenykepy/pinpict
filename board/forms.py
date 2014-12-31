from django import forms
from django.db import models

from haystack.forms import ModelSearchForm
from board.models import Board



class Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.label_suffix=''



class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.label_suffix=''



class UpdateBoardForm(ModelForm):
    """Board creation and edition form."""
    def __init__(self, *args, **kwargs):
        super(UpdateBoardForm, self).__init__(*args, **kwargs)
        self.fields['policy'].empty_label = None

    class Meta:
        model = Board
        fields = ('title', 'pins_order', 'reverse_pins_order', 'policy',
                'description', 'pin_default_description')


class BoardForm(ModelForm):
    """Private board creation form."""
    class Meta:
        model = Board
        fields = ('title', 'description')



class BoardSearchForm(ModelSearchForm):
    """Board search form."""

    def get_models(self):
        return [models.get_model('board.board')]
