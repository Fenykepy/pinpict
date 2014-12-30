from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from haystack.views import SearchView, search_view_factory
from haystack.query import SearchQuerySet
from haystack.forms import ModelSearchForm

from pin.forms import PinSearchForm
from pin.views import *
from pin.models import Pin

urlpatterns = patterns('',

        ## pin creation
        # create pin itself
        url(r'^create/$', 'pin.views.create_pin', name='create_pin'),

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

        # search engine
        url(r'^my_pins/search/page/(?P<page>\d+)/', search_view_factory(
                view_class=UserSearchView,
                template='pin/pin_my_search.html',
                form_class=PinSearchForm,
                searchqueryset=SearchQuerySet().models(Pin),
            ),
            name='my_pin_search'),
        url(r'^my_pins/search/', search_view_factory(
                view_class=UserSearchView,
                template='pin/pin_my_search.html',
                form_class=PinSearchForm,
                searchqueryset=SearchQuerySet().models(Pin),
            ),
            name='my_pin_search'),


        url(r'^search/page/(?P<page>\d+)/', search_view_factory(
                view_class=SearchView,
                template='pin/pin_search.html',
                form_class=PinSearchForm
            ),
            name='pin_search'),
        url(r'^search/', search_view_factory(
                view_class=SearchView,
                template='pin/pin_search.html',
                form_class=PinSearchForm
            ),
            name='pin_search'),

        ## view a pin
        url(r'^(?P<pk>\d+)/$',
            PinView.as_view(), name='pin_view'),

        ## update a pin
        url(r'^(?P<pk>\d+)/edit/$',
            login_required(UpdatePin.as_view()), name='update_pin'),

        ## delete a pin
        url(r'^(?P<pk>\d+)/delete/$',
            login_required(DeletePin.as_view()), name='pin_delete'),

        ## rate a pin
        url(r'^(?P<pk>\d+)/rate/(?P<rate>[0-5])/$',
            'pin.views.rate_pin', name="pin_rate"),

)
