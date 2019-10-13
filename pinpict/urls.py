from django.conf import settings
from django.conf.urls import include, url

from pinpict import views


urlpatterns = [
    
    ## drf api
    url('^api/$', views.api_root, name='api-root'),

    ## drf auth endpoints
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    ## Users endpoints
    url(r'^api/users/', include('user.urls')), # users API

    ## Pins endpoints
    url(r'^api/pins/', include('pin.urls')),

    ## Boards endpoints
    url(r'^api/boards/', include('board.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
