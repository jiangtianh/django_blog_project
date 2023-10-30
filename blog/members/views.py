from typing import Any
from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy

from .forms import SignUpForm, AccountSettingForm, PasswordChangingForm, ProfilePageForm
from django.contrib.auth.views import PasswordChangeView

from app_blog.models import Profile, Post
from django.shortcuts import get_object_or_404

class ShowProfilePageView(generic.DetailView):
    model = Profile 
    template_name = "registration/user_profile.html"

    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]:
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user

        posts = Post.objects.filter(author=page_user.user.pk).order_by('-post_created_date')
        context["posts"] = posts
        return context




class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('password_success')

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = AccountSettingForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
    

def password_success(request):
    return render(request, 'registration/password_success.html', {})


class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    form_class = ProfilePageForm
    success_url = reverse_lazy('home') 



class CreateProfilePageView(generic.CreateView):
    model = Profile
    template_name = 'registration/create_user_profile_page.html'
    form_class = ProfilePageForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
