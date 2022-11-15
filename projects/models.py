from email.policy import default
from enum import unique
from django.db import models
import uuid

from users.models import Profile
# Create your models here.





class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True , null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, unique=True,editable=False)
    created = models.DateTimeField(auto_now_add=True)
    demo_link = models.CharField(max_length=200,blank=True,null=True)
    source_link = models.CharField(max_length=200,blank=True,null=True)
    tags = models.ManyToManyField('Tag',blank=True,)
    vote_total = models.IntegerField(default=0,blank=True,null=True)
    vote_ratio = models.IntegerField(default=0,blank=True,null=True)
    featured_image = models.ImageField(default='default.jpg',blank=True,null=True,upload_to='%y/%m/%d')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio','-vote_total','title']
     
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
    
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = '/images/default.jpg'
        return url
       
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        
        ratio = (upVotes/totalVotes)*100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        
        self.save()
        


class Review(models.Model):
    owner = models.ForeignKey(Profile , on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE, blank=True , null=True)
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down','Down Vote'),
    )
    body = models.TextField(max_length=200,blank=True,null=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, unique=True,editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together = [['owner','project']]
        
    
        
    def __str__(self):
        return self.value
    
    
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, unique=True,editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name