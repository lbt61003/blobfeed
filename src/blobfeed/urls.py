"""blobfeed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from profiles.views import (
							HomeView,
							UserRegisterView
							)

from posts.views import (
                        HomeViewNew,
                        )
urlpatterns = [
    url(r'^admin/', admin.site.urls), #admin/
    url(r'^$', HomeViewNew.as_view(), name='home'), #/

    url(r'^post/', include('posts.urls', namespace='posts')),
    url(r'^api/post/', include('posts.api.urls', namespace='post-api')),
	url(r'^register/$', UserRegisterView.as_view(), name='register'), #/
    url(r'^api/', include('profiles.api.urls', namespace='profiles-api')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('profiles.urls', namespace='profiles')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
