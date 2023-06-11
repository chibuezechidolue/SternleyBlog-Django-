from django import forms
from Blog.models import BlogPost, Comments
class CreateBlogPost(forms.Form):
    title=forms.CharField(max_length=1000)
    subtitle=forms.CharField(max_length=250)
    img_url=forms.URLField()
    content=forms.CharField(widget=forms.Textarea())


    class Meta:
        model=BlogPost
        fields=['title','subtitle','img_url','content']

class EditBlogPost(forms.ModelForm):
    title=forms.CharField(max_length=1000)
    subtitle=forms.CharField(max_length=250)
    img_url=forms.URLField()
    content=forms.CharField(widget=forms.Textarea())


    class Meta:
        model=BlogPost
        fields=['title','subtitle','img_url','content']

class CommentForm(forms.Form):
    comment=forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model=Comments

