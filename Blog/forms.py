from dataclasses import field, fields
from django import forms
from Blog.models import  Comments
from django.core.mail import send_mail
from django.contrib import messages
import os
from dotenv import load_dotenv

load_dotenv()



class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comments
        fields=["comment"]


class ContactForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    phone=forms.IntegerField()
    content=forms.CharField(widget=forms.Textarea)

    def send_email(self):
        email = self.cleaned_data.get("email")
        name = self.cleaned_data.get("name")
        message = self.cleaned_data.get("content")
        phone = self.cleaned_data.get("phone")
    
        send_mail(
                subject='Message from SternleyBlog',
                message=f"\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}",
                from_email=None,
                recipient_list=[os.environ.get("RECEIVING_EMAIL"),],
                

            )

