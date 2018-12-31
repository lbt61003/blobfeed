from django.conf.urls import url

from django.views.generic.base import RedirectView

from .views import (
    LikeToggleAPIView,
    #RetweetAPIView,
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    )

app_name = "post-api"

urlpatterns = [
    # url(r'^$', RedirectView.as_view(url="/")), 
    url(r'^$', PostListAPIView.as_view(), name='list'), # /api/post/
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'), # /tweet/create/
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'),
    #url(r'^(?P<pk>\d+)/retweet/$', RetweetAPIView.as_view(), name='retweet'), #/api/post/id/tweet/
    # url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'), # /tweet/1/
    # url(r'^(?P<pk>\d+)/update/$', PostUpdateView.as_view(), name='update'), # /tweet/1/update/
    # url(r'^(?P<pk>\d+)/delete/$', PostDeleteView.as_view(), name='delete'), # /tweet/1/delete/
]