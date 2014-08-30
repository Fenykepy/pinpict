from board.forms import ModelForm

from pin.models import Pin


class PinForm(ModelForm):
    """Pin creation and edition form."""
    class Meta:
        model = Pin
