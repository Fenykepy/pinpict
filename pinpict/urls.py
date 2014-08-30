from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required

from board.views import *
from pin.views import ListPins

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinpict.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## administration
    url(r'^admin/', include(admin.site.urls)),

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
