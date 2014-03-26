from queue.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)
  
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password', \
              'confirm_password')

  def clean_confirm_password(self):
    password1 = self.cleaned_data['password']
    password2 = self.cleaned_data['confirm_password']
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("Password Mismatch")
    return password2

class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ()
