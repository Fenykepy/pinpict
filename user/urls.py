from django.conf.urls import url

from user import views


urlpatterns = [
        url(r'^current/$', views.CurrentUserDetail.as_view(),
            name="current-user"),
        url(r'public/(?P<slug>[-\w]+)/$', views.PublicUserDetail.as_view(),
            name="public-user"),
]


