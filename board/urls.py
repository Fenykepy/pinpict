from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from haystack.views import SearchView, search_view_factory

from board.forms import BoardSearchForm
from board.views import CreateBoard, CreatePrivateBoard, getCoversList

urlpatterns = patterns('',

    ## covers list
    url(r'^covers/(?P<pk>\d+)/', getCoversList, name='get_covers_list'),


    ### board creation
    ## public board creation
    url(r'^create/$', login_required(CreateBoard.as_view()),
        name='board_create'), 

    ## private board creation
    url(r'^create/private/$', login_required(CreatePrivateBoard.as_view()),
        name='private_board_create'),

        # search engine
        url(r'^search/page/(?P<page>\d+)/', search_view_factory(
                view_class=SearchView,
                template='board/board_search.html',
                form_class=BoardSearchForm
            ),
            name='board_search'),
        url(r'^search/', search_view_factory(
                view_class=SearchView,
                template='board/board_search.html',
                form_class=BoardSearchForm
            ),
            name='board_search'),
)
