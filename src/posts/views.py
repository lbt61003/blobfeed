from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import (
                CreateView,
                DetailView,
                DeleteView, 
                ListView, 
                UpdateView
                )

from .forms import PostForm
#from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Post
from profiles.models import UserProfile

class PostCreateView(CreateView):
    queryset = Post.objects.all()

class PostDetailView(DetailView):
    #pass
    queryset = Post.objects.all()

class HomeViewNew(LoginRequiredMixin, ListView):
    
    def get_queryset(self, *args, **kwargs):
        profile = self.request.user.profile
        print(profile)
        qs = Post.objects.all()
        #qs = UserProfile.objects.all()
        # query = self.request.GET.get("q", None)
        # if query is not None:
        #     qs = qs.filter(
        #             Q(content__icontains=query) |
        #             Q(user__username__icontains=query)
        #             )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(HomeViewNew, self).get_context_data(*args, **kwargs)
        context['create_form'] = PostForm()
        context['create_url'] = reverse_lazy("posts:create")
        print("HomeViewNew::get_context_data", context['create_url'])
        return context
