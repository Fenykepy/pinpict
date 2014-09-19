from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from user.models import User
from user.forms import *


class LoginView(FormView):
    """Class to login a user."""
    form_class = LoginForm
    template_name = 'user/user_login.html'
    
    def get(self, request, *args, **kwargs):
        """If user is logged in, redirect to it's board page."""
        if self.request.user.is_authenticated():
            return redirect(reverse_lazy('boards_list',
                kwargs={
                    'user': self.request.user.slug,
                }))
        return super(LoginView, self).get(self, request, *args, **kwargs)


    def form_valid(self, form):
        login(self.request, form.get_user()) # connect user
        
        url = self.request.GET.get('next', False)
        if url:
            return redirect(url)
        else:
            return redirect(reverse_lazy('boards_list',
                kwargs={
                    'user': self.request.user.slug,
                }))


def logout_view(request):
    """View to log user out."""
    logout(request)
    return redirect(reverse_lazy('user_login'))


class RegistrationView(FormView):
    """Class to register a user."""
    form_class = RegistrationForm
    template_name = 'user/user_registration.html'


    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]

        user = authenticate(username=username, password=password)

        # send mail to admin and user here

        return redirect(reverse_lazy('boards_list',
            kwargs={
                'user': user.slug,
            }))
