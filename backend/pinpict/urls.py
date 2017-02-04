from django.conf.urls import include, url

from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap



urlpatterns = [
    # Examples:
    # url(r'^$', 'pinpict.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## rest api
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/users/', include('user.urls')), # users API
    url(r'^api/pin/', include('pin.urls')),

]

