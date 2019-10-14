from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from pin import views

urlpatterns = [
        url('^menu/$', views.pin_root, name='pin-root'),
        url('^tags/$', views.tags_flat_list, name='tags-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
