from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from pinpict.sitemaps import UserSitemap, BoardSitemap, PinSitemap
from board.views import *
from user.views import LoginView, RegistrationView, ProfilView, \
        PasswordView, RecoveryView
from pin.views import ListBoardPins, ListUserPins, ListLastPins

admin.autodiscover()

sitemaps = {
    'users': UserSitemap,
    'boards': BoardSitemap,
    'pins': PinSitemap,
}


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinpict.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## administration
    url(r'^admin/', include(admin.site.urls)),

    ## site map
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),

    ## user management
    ## login
    url(r'^login/$', LoginView.as_view(), name='user_login'),

    ## logout
    url(r'^logout/$', 'user.views.logout_view', name='user_logout'),

    ## registration
    url(r'^register/$', RegistrationView.as_view(), name='user_registration'),

    ## password recovery
    url(r'^recovery/$', RecoveryView.as_view(), name='user_recovery'),
    url(r'^recovery/(?P<uuid>[-\w]+)/$', 'user.views.confirm_recovery_view', name='user_confirm_recovery'),

    ## profil
    url(r'^profil/$', login_required(ProfilView.as_view()), name='user_profil'),

    ## password changement
    url(r'^profil/password/$', login_required(PasswordView.as_view()), name='user_password'),
    
    ## home page with pagination
    url(r'^page/(?P<page>\d+)/$',
        login_required(ListLastPins.as_view()), name='home'),


    ## user pins list
    url(r'^(?P<user>[-\w]+)/pins/page/(?P<page>\d+)/$',
        ListUserPins.as_view(), name='user_pins'),
    url(r'^(?P<user>[-\w]+)/pins/$',
        ListUserPins.as_view(), name='user_pins'),



    ## home page
    url(r'^$', login_required(ListLastPins.as_view()), name='home'),

    ## user urls
    url(r'^user/', include('user.urls')),

    ## pin urls
    url(r'^pin/', include('pin.urls')),

    ## board urls
    url(r'^board/', include('board.urls')),

    ## board list
    url(r'^(?P<user>[-\w]+)/$',
        ListBoards.as_view(), name='boards_list'),

    ## pin list
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/page/(?P<page>\d+)/$',
        ListBoardPins.as_view(), name='board_view'),
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/$',
        ListBoardPins.as_view(), name='board_view'),

    ## board update
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/edit/$',
        login_required(UpdateBoard.as_view()),
        name='board_update'),

    ## board delete
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/delete/$',
        login_required(DeleteBoard.as_view()),
        name='board_delete'),
)

# to test error templates
if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^403/$', TemplateView.as_view(template_name='403.html')),
        (r'^404/$', TemplateView.as_view(template_name='404.html')),
        (r'^500/$', TemplateView.as_view(template_name='500.html')),
    ) + urlpatterns

# To get static files during development
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
