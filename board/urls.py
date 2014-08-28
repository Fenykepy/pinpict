from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from board.views import CreateBoard, UpdateBoard, DeleteBoard

urlpatterns = patterns('',
        url(r'^create/$', login_required(CreateBoard.as_view()),
            name='board_create'),
        url(r'^update/(?P<board>[-\w]+)/$',
            login_required(UpdateBoard.as_view()),
            name='board_update'),
        url(r'^delete/(?P<board>[-\w]+)/$',
            login_required(UpdateBoard.as_view()),
            name='board_delete'),
)
