from django.conf.urls import patterns, url

from pin.views import *

urlpatterns = patterns('',
        url(r'^(?P<pk>[-\w]+)/$',
            PinView.as_view(), name='pin_view'),
)
