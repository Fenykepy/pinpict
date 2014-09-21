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


    def dispatch(self, request, *args, **kwargs):
        # if user is logged in, redirect to it's home page
        if request.user.is_authenticated():
            return redirect(reverse_lazy('boards_list',
                kwargs={
                    'user': request.user.slug,
                }))
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]

        user = authenticate(username=username, password=password)
        # login user
        login(self.request, user)

        # send mail to admin and user here

        return redirect(reverse_lazy('boards_list',
            kwargs={
                'user': user.slug,
            }))


class ProfilView(UpdateView):
    """Class to update user profil."""
    form_class = ProfilForm
    model = User
    template_name = 'board/board_forms.html'

    def get_object(self, queryset=None):
        """Returns object view is displaying."""
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfilView, self).get_context_data(**kwargs)
        context['title'] = 'Update my profil'
        context['button'] = 'Save'

        return context

    def get_success_url(self):
        return reverse_lazy('boards_list',
                kwargs={'user': self.request.user.slug})


class PasswordView(FormView):
    """Class to register a user."""
    form_class = PasswordForm
    template_name = 'board/board_forms.html'


    def form_valid(self, form):
        password = form.cleaned_data["password1"]

        self.request.user.set_password(password)
        self.request.user.save()


        # send mail to admin and user here
        return redirect(reverse_lazy('boards_list',
            kwargs={
                'user': self.request.user.slug,
            }))

    def get_context_data(self, **kwargs):
        context = super(PasswordView, self).get_context_data(**kwargs)
        context['title'] = 'Change my password'
        context['button'] = 'Save'

        return context



