from queue.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password')

class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ('website',)
