from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from haystack.views import SearchView, search_view_factory
from user.forms import UserSearchForm
from user.views import *


urlpatterns = [
    ## add and remove follower
    url(r'^follow/(?P<pk>\d+)/', userFollow,
        name='user_follow'),
    url(r'^unfollow/(?P<pk>\d+)/', userUnfollow,
        name='user_unfollow'),

    ## add and remove pin like
    url(r'^like/(?P<pk>\d+)/', likePin,
        name='user_like_pin'),
    url(r'^unlike/(?P<pk>\d+)/', unlikePin,
        name='user_unlike_pin'),

    ## search engine
    url(r'^search/page/(?P<page>\d+)/', login_required(search_view_factory(
            view_class=SearchView,
            template='user/user_search.html',
            form_class=UserSearchForm
        )),
        name='user_search'),
    url(r'^search/', login_required(search_view_factory(
            view_class=SearchView,
            template='user/user_search.html',
            form_class=UserSearchForm
        )),
        name='user_search'),
]


