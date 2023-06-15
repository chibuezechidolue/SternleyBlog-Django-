from django.db import models
from User.models import CustomUser
from django.urls import reverse

global BlogPost


class BlogPost(models.Model):
    title = models.CharField(max_length=1000)
    subtitle = models.CharField(max_length=250)
    date = models.DateField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    img_url = models.URLField()

    def __str__(self) -> str:
        return self.subtitle


# if success_url is not defined in the CreatePostView
# def get_absolute_url(self):
#     return reverse('home-page')


class Comments(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
