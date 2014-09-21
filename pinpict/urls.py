from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from board.views import *
from user.views import LoginView, RegistrationView, ProfilView, \
        PasswordView
from pin.views import ListPins

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinpict.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## administration
    url(r'^admin/', include(admin.site.urls)),

    ## user management
    ## login
    url(r'^login/$', LoginView.as_view(), name='user_login'),

    ## logout
    url(r'^logout/$', 'user.views.logout_view', name='user_logout'),

    ## registration
    url(r'^register/$', RegistrationView.as_view(), name='user_registration'),

    ## profil
    url(r'^profil/$', login_required(ProfilView.as_view()), name='user_profil'),

    ## password changement
    url(r'^profil/password/$', login_required(PasswordView.as_view()), name='user_password'),


    ## home page
    url(r'^$', 'pinpict.views.home', name='home'),

    ### board creation
    ## public board creation
    url(r'^board/create/$', login_required(CreateBoard.as_view()),
        name='board_create'),

    ## private board creation
    url(r'^board/create/private/$', login_required(CreatePrivateBoard.as_view()),
        name='private_board_create'),

    ## pin urls
    url(r'^pin/', include('pin.urls')),

    ## board list
    url(r'^(?P<user>[-\w]+)/$',
        ListBoards.as_view(), name='boards_list'),

    ## pin list
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/$',
        ListPins.as_view(), name='board_view'),

    ## board update
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/edit/$',
        login_required(UpdateBoard.as_view()),
        name='board_update'),

    ## board delete
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/delete/$',
        login_required(DeleteBoard.as_view()),
        name='board_delete'),
)


# To get static files during development
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
