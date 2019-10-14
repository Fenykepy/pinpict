from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from pin import views

urlpatterns = [
        url('^menu/$', views.pin_root, name='pin-root'),
        url('^$', views.PinList.as_view(), name='pin-list'),
        url(r'^(?P<pk>\d+)/$', views.PinDetail.as_view(),
            name='pin-detail'),
        url('^tags/$', views.tags_flat_list, name='tag-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
