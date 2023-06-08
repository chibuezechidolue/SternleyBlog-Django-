from django.shortcuts import render
from . import forms

def register_page(request):
    form=forms.UserRegisterForm()

    return render(request,'user/register.html',{'form':form})


