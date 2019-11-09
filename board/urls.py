from django.conf.urls import url, include


from board import views

urlpatterns = [
    url(r'^menu/$', views.board_root, name='board-root'),

    url(r'^$', views.BoardList.as_view(),
        name='board-list'),

    url(r'^edit/user/(?P<user>[-\w]+)/board/(?P<board>[-\w]+)/$',
        views.BoardDetail.as_view(),
        name='board-detail'),

    url(r'^user/(?P<user>[-\w]+)/board/(?P<board>[-\w]+)/$',
        views.ShortBoardDetail.as_view(),
        name='short-board-detail'),

    url(r'^public/user/(?P<user>[-\w]+)/$', views.user_public_boards_list,
        name='user-public-boards-list'),

    url(r'^private/user/(?P<user>[-\w]+)/$', views.user_private_boards_list,
        name='user-private-boards-list'),
]
