from django.conf import settings
from django.conf.urls import include, url

from rest_framework_jwt.views import obtain_jwt_token, \
        verify_jwt_token

from pinpict.views import api_root


urlpatterns = [
    
    ## drf api
    url('^api/$', api_root, name='api-root'),

    ## drf auth endpoints
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    ## JWT management endpoints
    url(r'^api/token-auth/', obtain_jwt_token,
        name='token-auth'),
    url(r'^api/token-verify/', verify_jwt_token,
        name='token-verify'),
    
    ## Users endpoints
    url(r'^api/users/', include('user.urls')), # users API

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
