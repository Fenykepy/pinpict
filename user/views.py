import datetime

from uuid import uuid4
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from pinpict.settings import EMAIL_SUBJECT_PREFIX
from user.models import User, Notification, mail_staffmembers
from user.forms import *
from pin.views import ListPinsMixin

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
        
        # send mail to new user
        subject = '{} Welcome on pinpict'.format(EMAIL_SUBJECT_PREFIX)

        message = (
            "Welcome on pinpict {} !\n\n"
            "You can access to your page here:\n"
            "{}\n\n"
            "And set your profil up there:\n"
            "{}\n"
            "Good pinning !\n\n"
        ).format(
            username,
            self.request.build_absolute_uri(reverse('boards_list',
                kwargs={
                    'user': user.slug,
                })),
            self.request.build_absolute_uri(reverse('user_profil')),
        )

        user.send_mail(subject, message)

        # send mail to admins
        subject = '{} new registration'.format(EMAIL_SUBJECT_PREFIX)

        message = (
            "A new user registered on pinpict.\n"
            "username: {}\n"
            "email: {}\n"
            "page: {}\n"
        ).format(
            username,
            user.email,
            self.request.build_absolute_uri(reverse('boards_list',
                kwargs={
                    'user': user.slug,
                })),
        )
        mail_staffmembers(subject, message)



        return redirect(reverse_lazy('boards_list',
            kwargs={
                'user': user.slug,
            }))


class ProfilView(UpdateView):
    """Class to update user profil."""
    form_class = ProfilForm
    model = User
    template_name = 'user/user_profil.html'

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


class ListNotifications(ListView, ListPinsMixin):
    """List all notifications of an user."""
    model = Notification
    context_object_name = 'notifications'
    template_name = 'user/notifications_list.html'
    paginate_by = 100

    def get_queryset(self):
        return self.request.user.get_notifications()


class RecoveryView(FormView):
    """Class to ask for password recovery."""
    form_class = PasswordRecoveryForm
    template_name = 'user/user_recovery.html'


    def dispatch(self, request, *args, **kwargs):
        # if user is logged in, redirect to password changement page
        if request.user.is_authenticated():
            return redirect(reverse_lazy('user_password'))
        return super(RecoveryView, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        # get user object
        username = form.cleaned_data['username']
        user = User.objects.get(username=username)

        # set user uuid
        user.uuid = str(uuid4())
        # set user uuid expiration
        user.uuid_expiration = datetime.timedelta(1) + \
            datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
        
        # send mail with uuid
        subject = '[Pin Pict]Password Recovery'
        message = (
            "You may have asked for a password recovery on Pin Pict.\n"
            "If this request is from you, you can set a new password"
            " during 24 hours by following this link :\n"
            "http://{}/recovery/{}/\n"
        ).format(self.request.get_host(), user.uuid)

        user.send_mail(subject, message)

        user.save()

        
        return render(self.request, 'user/user_recovery.html', {'recovery': True})


def confirm_recovery_view(request, uuid):
    """Login and redirect to password changement page user who
    corresponds to given uuid, else return 404"""
    # get user wich correspond to uuid or return 404
    user = get_object_or_404(User, uuid=uuid)
    # compare dates
    now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    if user.uuid_expiration.timestamp() <  now.timestamp():
        raise Http404
    # login user if everything is ok
    # reset it's password to uuid
    password = str(uuid4())
    user.set_password(password)
    # reset user's uuid and uuid_expiration
    user.uuid = None
    user.uuid_expiration = None
    user.save()
    user = authenticate(username=user.username, password=password)
    login(request, user)
    
    # redirect to password changement form
    return redirect(reverse_lazy('user_password'))


@login_required
def userFollow(request, pk):
    """Add a follower to an user."""
    if not request.is_ajax():
        raise Http404
    user = get_object_or_404(User, id=pk)
    user.add_follower(request.user)

    return HttpResponse(reverse_lazy('user_unfollow',
        kwargs={'pk': pk}))


@login_required
def userUnfollow(request, pk):
    """Remove a follower from an user."""
    if not request.is_ajax():
        raise Http404
    user = get_object_or_404(User, id=pk)
    user.remove_follower(request.user)

    return HttpResponse(reverse_lazy('user_follow',
        kwargs={'pk': pk}))

