from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from app_blog.models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email Address", required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    first_name = forms.CharField(label="First Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label="Last Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class AccountSettingForm(UserChangeForm):
    username = forms.CharField(label="Username", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    email = forms.EmailField(label="Email Address", required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    first_name = forms.CharField(label="First Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label="Last Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        help_texts = "Raw passwords are not stored, so there is no way to see this user’s password, but you can change the password using <a href='{}'>this form</a>.".format(reverse('change_password'))
    
        self.fields['password'].help_text = format_html(help_texts)
    
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter old password'}))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password again'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
    


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter bio'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'website_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter website url'}),
            'facebook_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter facebook url'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter twitter url'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter instagram url'}),
            'pinterest_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pinterest url'}),
        }

