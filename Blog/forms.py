from django import forms
from Blog.models import BlogPost, Comments



class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comments
