from django.urls import reverse
from . import forms
from User.models import CustomUser, Profile
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.views.generic import ListView,CreateView,DeleteView,UpdateView,TemplateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin



class RegisterPage(SuccessMessageMixin,CreateView):
    model=CustomUser
    # fields=['first_name','last_name','username','email','phone_no',"password",]
    form_class=forms.UserRegisterForm
    template_name="user/register.html"
    success_message="Your account has been created"
    success_url="login/"


class ProfilePage(LoginRequiredMixin,TemplateView):
    template_name="user/profile.html"


class UpdateProfilePage(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Profile
    template_name='user/profile-update.html'
    form_class=forms.ProfileUdateForm
    second_form_class=forms.UserUdateForm

    def get_context_data(self, **kwargs):
        kwargs['active_client'] = True
        kwargs['form2'] =self.second_form_class(instance=self.get_object().user)
        return super(UpdateProfilePage, self).get_context_data(**kwargs)


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,instance=request.user.profile)
        form2 = self.second_form_class(request.POST,instance=request.user)
        if form.is_valid() and form2.is_valid():
            profiledata = form.save(commit=False)
            profiledata.save()
            userdata = form2.save(commit=False)
            userdata.save()
            # messages.add_message(request,messages.SUCCESS, 'Settings saved successfully')
            return super().post(request, *args, **kwargs)
        else:
            return self.render_to_response(
              self.get_context_data(form=form, form2=form2))
        
    def get_success_url(self):
        return reverse('profile-page')
    
    def test_func(self):
        profile=self.get_object()
        if self.request.user==profile.user:
            return True
        else:
            return False