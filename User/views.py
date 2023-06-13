from urllib import request
from django.shortcuts import render, redirect
from . import forms
from Blog.models import BlogPost
from User.models import Profile
from django.contrib.auth.decorators import login_required 
from django.contrib import messages



def register_page(request):
    form = forms.UserRegisterForm()

    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)

        if form.is_valid():
            print("is valid")
            form.save()
            messages.add_message(request, messages.SUCCESS, "Your account has been created")
            return redirect("login")

    return render(request, "user/register.html", {"form": form})

@login_required
def profile_page(request):
    return render(request,"user/profile.html")

@login_required
def profile_update_page(request):
    user_form=forms.UserUdateForm(instance=request.user)
    profile_form=forms.ProfileUdateForm(instance=request.user.profile)
    if request.method=="POST":
        user_form=forms.UserUdateForm(request.POST,instance=request.user)
        profile_form=forms.ProfileUdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.add_message(request, messages.SUCCESS, "Your profile has been updated")

            return redirect('profile-page')


    return render(request,'user/profile-update.html',{"user_form": user_form, "profile_form":profile_form})
    
