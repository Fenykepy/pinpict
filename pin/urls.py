from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from pin.views import *

urlpatterns = patterns('',

        ## pin creation
        # create pin itself
        url(r'^create/(?P<resource>\d+)/$',
            login_required(CreatePin.as_view()), name='create_pin'),

        # choose pin file origin
        url(r'^choose-origin/$',
            login_required(ChoosePinOrigin.as_view()),
            name='choose_origin_pin'),

        # upload pin file from computer
        url(r'^upload/$',
            login_required(UploadPin.as_view()), name='pin_upload'),

        # select url
        url(r'^url/$',
            login_required(ChoosePinUrl.as_view()), name='choose_pin_url'),

        # select pin
        url(r'^find/$',
            login_required(FindPin.as_view()), name='find_pin'),


        ## view a pin
        url(r'^(?P<pk>\d+)/$',
            PinView.as_view(), name='pin_view'),

        ## update a pin
        url(r'^(?P<pk>\d+)/edit/$',
            login_required(UpdatePin.as_view()), name='update_pin'),

        ## delete a pin
        url(r'^(?P<pk>\d+)/delete/$',
            login_required(DeletePin.as_view()), name='pin_delete'),
)
