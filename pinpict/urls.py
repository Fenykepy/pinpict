from django.conf import settings
from django.conf.urls import include, url

from pinpict import views


urlpatterns = [
    
    ## drf api
    url('^api/$', views.api_root, name='api-root'),

    ## drf auth endpoints
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    ## Users endpoints
    url(r'^api/user/', include('user.urls')), # users API

    ## Pins endpoints
    url(r'^api/pin/', include('pin.urls')),

    ## Boards endpoints
    url(r'^api/board/', include('board.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
