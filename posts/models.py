from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = []  

class Post(models.Model):
    
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    header = models.CharField(max_length=120,default="")
    body = models.TextField(default="") 