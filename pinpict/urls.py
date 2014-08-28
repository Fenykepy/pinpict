from django.conf.urls import patterns, include, url

from django.contrib import admin

from board.views import PinView, ListBoards, ListPins

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinpict.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^board/', include('board.urls')),
    url(r'^$', 'pinpict.views.home', name='home'),
    url(r'^pin/(?P<pk>[-\w]+)/$',
        PinView.as_view(), name='pin_view'),
    url(r'^(?P<user>[-\w]+)/$',
        ListBoards.as_view(), name='boards_list'),
    url(r'^(?P<user>[-\w]+)/(?P<board>[-\w]+)/$',
        ListPins.as_view(), name='board_view'),
)
