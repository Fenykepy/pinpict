from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from pinpict.sitemaps import UserSitemap, BoardSitemap, PinSitemap
from board.views import *
from pin.views import ListBoardPins, ListUserPins, ListLastPins

sitemaps = {
    'users': UserSitemap,
    'boards': BoardSitemap,
    'pins': PinSitemap,
}


urlpatterns = [
    # Examples:
    # url(r'^$', 'pinpict.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## rest api
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/users/', include('user.urls')), # users API
    url(r'^api/pin/', include('pin.urls')),

    ## site map
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': sitemaps}),


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
]

# To get static files during development
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
