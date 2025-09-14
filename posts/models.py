from django.db import models

class Post(models.Model):
    
    header = models.CharField(max_length=120,default="")
    body = models.TextField(default="") 