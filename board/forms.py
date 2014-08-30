from django import forms

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
    class Meta:
        model = Board
        fields = ('title', 'description', 'policy')


class BoardForm(ModelForm):
    """Private board creation form."""
    class Meta:
        model = Board
        fields = ('title', 'description')


