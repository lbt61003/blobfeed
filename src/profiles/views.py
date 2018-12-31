from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import View
from django.views.generic import (
					DetailView,
					ListView,
					UpdateView
					)

from django.views.generic.edit import FormView

from .forms import UserRegisterForm
from .models import UserProfile

# Create your views here.

User = get_user_model()

class UserRegisterView(FormView):
    template_name = 'profiles/user_register_form.html'
    form_class = UserRegisterForm
    success_url = '/login'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return super(UserRegisterView, self).form_valid(form)

class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)
        # url = reverse("profiles:detail", kwargs={"username": username})
        # HttpResponseRedirect(url)

class UserDetailView(DetailView):
    template_name = 'profiles/profile_detail.html'
    queryset = User.objects.all()
    
    def get_object(self):
        return get_object_or_404(
                    User, 
                    username__iexact=self.kwargs.get("username")
                    )
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        context['recommended'] = UserProfile.objects.recommended(self.request.user)
        return context

class HomeView(View):
	def get(self, request, *args, **kwargs):

		if not request.user.is_authenticated:
			object_list = UserProfile.objects.all()
			return render(request, "home.html", {"object_list": object_list})

		user = request.user
		profile = request.user.profile
		is_following_user_ids = [x.user.id for x in profile.get_following()]
		qs = UserProfile.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-updated")[:3]
		return render(request, "home.html", {'object_list': qs})

