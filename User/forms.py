from django.contrib.auth.forms import UserCreationForm
from django import forms
from User.models import CustomUser,Profile

class UserRegisterForm(UserCreationForm):
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()
    phone_no=forms.IntegerField()
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','username','email','phone_no']


class ProfileUdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image','bio',]

class UserUdateForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['username','email','phone_no']