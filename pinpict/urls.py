from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required

from board.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinpict.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'pinpict.views.home', name='home'),
    url(r'^board/create/$', login_required(CreateBoard.as_view()),
        name='board_create'),
    url(r'^board/create/private/$', login_required(CreatePrivateBoard.as_view()),
        name='private_board_create'),
    url(r'^pin/(?P<pk>[-\w]+)/$',
        PinView.as_view(), name='pin_view'),
    url(r'^(?P<user>[-\w]+)/$',
        ListBoards.as_view(), name='boards_list'),
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/$',
        ListPins.as_view(), name='board_view'),
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/edit/$',
        login_required(UpdateBoard.as_view()),
        name='board_update'),
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/delete/$',
        login_required(DeleteBoard.as_view()),
        name='board_delete'),
)
