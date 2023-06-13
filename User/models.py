from email.mime import image
from tkinter import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class CustomUser(AbstractUser):
    phone_no=models.IntegerField(null=True)
    email=models.EmailField(unique=True)
   

class Profile(models.Model):
     image=models.ImageField(default='default.jpg',upload_to='profile-pics')
     bio=models.TextField()
     user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)

     def __str__(self) -> str:
          return f"{self.user.username} profile"
     
     def save(self, *args,**kwargs):
          super().save(*args,**kwargs)
          img=Image.open(self.image.path)
          if img.height>300 or img.width>300:
               output_size=(300,300)
               img.thumbnail(output_size)
               if img.height/img.width<0.75:
                    img=img.transpose(Image.ROTATE_270)
          img.save(self.image.path)               
               
          

     

    
    




