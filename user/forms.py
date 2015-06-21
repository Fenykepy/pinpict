from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models

from haystack.forms import ModelSearchForm

from board.forms import Form, ModelForm
from user.models import User
from pinpict.settings import RESERVED_WORDS



class LoginForm(Form, AuthenticationForm):
    """Form to login a user."""

    username = forms.CharField(
            max_length=254,
            widget=forms.TextInput(attrs={
                'placeholder': 'Username',
                'required': 'required'
            }
        ))
    password = forms.CharField(
            label=_("Password"),
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'required': 'required'
            }
        ))


class RegistrationForm(ModelForm):
    """Form to create a user, with no privilege."""

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                "@/./+/-/_ only."),
        widget=forms.TextInput(attrs={
            'placeholder': 'username', 
            'required': 'required', 
            'pattern': '[\w.@+-]+$'
        }),
        error_messages={
                'invalid': _("This value may contain only letters, numbers and "
                    "@/./+/-/_ characters.")})
    email = forms.EmailField(
            label=_("Email"),
            widget=forms.EmailInput(attrs={
                'placeholder': 'email',
                'required': 'required'
            }
        ))
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password',
            'required': 'required'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password confirmation',
            'required': 'required'}),
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        if username in RESERVED_WORDS:
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
        )
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True



class PasswordForm(Form):
    """Password changement form."""
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password',
            'required': 'required'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password confirmation',
            'required': 'required'}),
        help_text=_("Enter the same password as above, for verification."))


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class ProfilForm(ModelForm):
    """Profil edition form."""

    def __init__(self, *args, **kwargs):
        super(ProfilForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'avatar',
            'website',
            'facebook_link',
            'flickr_link',
            'px500_link',
            'twitter_link',
            'gplus_link',
            'pinterest_link',
            'vk_link',
            'instagram_link',
            'mail_user_follower',
            'mail_board_follower',
            'mail_following_add_pin',
            'mail_following_add_board',
            'mail_repinned',
            'mail_allow_read',
        )


class PasswordRecoveryForm(Form):
    """Form to recovery password."""

    username = forms.CharField(
            max_length=254,
            widget=forms.TextInput(attrs={
                'placeholder': 'Username',
                'required': 'required'
            }
        ))

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(
                'Invalid username.'
            )
        return username


class UserSearchForm(ModelSearchForm):
    """User search form."""

    def get_models(self):
        return [models.get_model('user.user')]
