from django.conf.urls import patterns, url
from board.views import *

urlpatterns = patterns('',
        url(r'^pin/(?P<uniqid>[-\w]+)/$',
            'board.views.view_pin', name='pin_view'),
        url(r'^(?P<user>[-\w]+)/$',
            ListBoards.as_view(), name='boards_list'),
        url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/$',
            'board.views.view_board', name='board_view'),
)
