from django.conf.urls import patterns, url
from board.views import *

urlpatterns = patterns('',
        url(r'^pin/(?P<uniqid>[-\w]+)/$',
            PinView.as_view(), name='pin_view'),
        url(r'^(?P<user>[-\w]+)/$',
            ListBoards.as_view(), name='boards_list'),
        url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/$',
            ListPins.as_view(), name='board_view'),
)
