from django import forms
import datetime
from Blog.models import BlogPost
class CreateBlogPost(forms.Form):
    title=forms.CharField(max_length=1000)
    subtitle=forms.CharField(max_length=250)
    img_url=forms.URLField()
    content=forms.CharField(widget=forms.Textarea())


    class Meta:
        model=BlogPost
        ordering=['title','subtitle','content','img_url']
# 