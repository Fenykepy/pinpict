from django.conf.urls import url, include


from board import views

urlpatterns = [
    url(r'^menu/$', views.board_root, name='board-root'),
    url(r'^$', views.BoardsList.as_view(),
        name='boards-list'),
]
