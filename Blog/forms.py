from django import forms
from Blog.models import BlogPost, Comments


class CreateBlogPost(forms.Form):
    title = forms.CharField(
        max_length=1000,
        error_messages={
            "required": "Please enter the title",
            "min_length": "title must be above 5 characters",
        },
        min_length=6,
    )
    subtitle = forms.CharField(max_length=250)
    img_url = forms.URLField()
    content = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = BlogPost
        fields = ["title", "subtitle", "img_url", "content"]


class EditBlogPost(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "subtitle", "img_url", "content"]


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comments
