from django.conf.urls import url
from rest_framework_simplejwt.views import (
        TokenRefreshView,
)

from user import views


urlpatterns = [
        url(r'^token/$', views.SlugTokenObtainPairView.as_view(), name="token-obtain"),
        url(r'^token/refresh/$', TokenRefreshView.as_view(), name="token-refresh"),
        url(r'^current/$', views.CurrentUserDetail.as_view(),
            name="current-user"),
        url(r'^menu/$', views.user_root, name='user-root'),
        url(r'(?P<slug>[-\w]+)/public/$', views.PublicUserDetail.as_view(),
            name="public-user"),
        url(r'(?P<slug>[-\w]+)/$', views.UserDetail.as_view(),
            name="user-detail"),
        url(r'^$', views.UserList.as_view(),
            name="user-list"),
]


