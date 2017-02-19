from django.conf.urls import url, include


from board import views

urlpatterns = [
    url(r'^menu/$', views.board_root, name='board-root'),
    url(r'^$', views.BoardsList.as_view(),
        name='boards-list'),
    url(r'^user/(?P<user>[-\w]+)/board/(?P<board>[-\w]+)/$',
        views.BoardDetail.as_view(),
        name='board-detail'),
    url(r'^user/(?P<user>[-\w]+)/$', views.user_public_boards_list,
        name='user-public-boards-list'),
    url(r'^private/user/(?P<user>[-\w]+)/$', views.user_private_boards_list,
        name='user-private-boards-list'),
]
