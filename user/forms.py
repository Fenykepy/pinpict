from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext, ugettext_lazy as _

from board.forms import Form, ModelForm
from user.models import User



class LoginForm(Form, AuthenticationForm):
    """Form to login a user."""

    username = forms.CharField(
            max_length=254,
            widget=forms.TextInput(attrs={
                'placeholder': 'Nom d\'utilisateur',
                'required': 'required'
            }
        ))
    password = forms.CharField(
            label=_("Password"),
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Mot de passe',
                'required': 'required'
            }
        ))



