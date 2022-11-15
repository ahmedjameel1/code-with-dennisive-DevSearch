from email.policy import default
from pydoc import describe
from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, blank=True , null=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    username = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(blank=True,null=True)
    short_intro = models.CharField(max_length=150,null=True,blank=True)
    bio = models.TextField(max_length=300,blank=True,null=True)
    location = models.CharField(max_length=50,null=True,blank=True)
    profile_image = models.ImageField(default='user-default.png', upload_to='profile_pics/%y/%m/%d')
    social_github = models.CharField(max_length=50,null=True,blank=True)
    social_twitter = models.CharField(max_length=50,null=True,blank=True)
    social_youtube = models.CharField(max_length=50,null=True,blank=True)
    social_website = models.CharField(max_length=50,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.username)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = '/images/user-default.png'
        return url
    
    class Meta:
        ordering = ['-created']

class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField(max_length=150,null=True,blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True , null=True)
    
    def __str__(self):
        return self.name
    



class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True , blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True , blank=True, related_name="messages")
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    is_read = models.BooleanField(default=False,null=True)
    body = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read','-created']