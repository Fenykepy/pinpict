from django.conf.urls import url, include


from board import views

urlpatterns = [
    url(r'^menu/$', views.board_root, name='board-root'),
    url(r'^$', views.BoardsList.as_view(),
        name='boards-list'),
    url(r'^user/(?P<user>[-\w]+)/$', views.UserPublicBoardsList.as_view(),
        name='user-public-boards-list'),
    url(r'^private/user/(?P<user>[-\w]+)/$', views.UserPrivateBoardsList.as_view(),
        name='user-private-boards-list'),
]
