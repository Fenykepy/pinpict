from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from pinpict.sitemaps import UserSitemap, BoardSitemap, PinSitemap

sitemaps = {
    'users': UserSitemap,
    'boards': BoardSitemap,
    'pins': PinSitemap,
}


urlpatterns = [
    # Examples:
    # url(r'^$', 'pinpict.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## rest api
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/users/', include('user.urls')), # users API
    url(r'^api/pin/', include('pin.urls')),

    ## site map
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': sitemaps}),
]

# To get static files during development
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)