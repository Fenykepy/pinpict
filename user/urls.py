from django.conf.urls import url
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
)

from user import views


urlpatterns = [
        url(r'^token/$', TokenObtainPairView.as_view(), name="token-obtain"),
        url(r'^token/refresh$', TokenRefreshView.as_view(), name="token-refresh"),
        url(r'^current/$', views.CurrentUserDetail.as_view(),
            name="current-user"),
        url(r'public/(?P<slug>[-\w]+)/$', views.PublicUserDetail.as_view(),
            name="public-user"),
        url(r'^$', views.user_root, name='user-root'),
]


