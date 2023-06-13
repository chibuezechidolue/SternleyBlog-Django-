from django.contrib import admin
from Blog.models import BlogPost,Comments

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Comments)