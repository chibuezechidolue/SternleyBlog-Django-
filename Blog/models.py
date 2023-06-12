from django.db import models
from User.models import CustomUser


class BlogPost(models.Model):
    title = models.CharField(max_length=1000)
    subtitle = models.CharField(max_length=250)
    date = models.DateField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    img_url = models.URLField()

    # comment=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.subtitle


class Comments(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
