from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import  Message, Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from projects.models import Review


@receiver(post_save, sender=User)
def createProfile(sender, instance ,created ,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )
        
        subject = f"Welcome {profile.name}!".title()
        message = f'\n\n\nhave fun on our website , explore more here http://127.0.0.1:8000/projects/'.title()
        
        
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [profile.email],
        #     fail_silently= False,
        # )
        
    
@receiver(post_delete, sender=Profile)
def deleteProfile(sender, instance,**kwargs):
    
    try:
        user = instance.user
        user.delete()
    except:
        pass


@receiver(post_save, sender=Message)
def messagenotifyGmail(sender , instance , **kwargs):
    recipient = instance.recipient
    subject = f"new message! on DevSearch!".title()
    message = f"hey {recipient.name} you have a new unread message! \n\n\nsubject: {instance.subject} \n\nMessage: {instance.body[1:15]}...\n\n\nPlease Login Here: 127.0.0.1:8000/inbox to View Your full unread Messages!".title()
        
        
    # send_mail(
    #             subject,
    #             message,
    #             settings.EMAIL_HOST_USER,
    #             [recipient.email],
    #             fail_silently= False,
    #             )
    
    
    
@receiver(post_save, sender=Review)
def reviewnotifyGmail(sender , instance , **kwargs):
    owner = instance.project.owner
    subject = f"you got a new {instance.value} review on your project {instance.project.title}!".title()
    message = f"Review: {instance.body[1:15]}...\n\n Please Login Here: 127.0.0.1:8000/projects/project/{instance.project.id} To View The Full Feedback!"
        
        
    # send_mail(
    #             subject,
    #             message,
    #             settings.EMAIL_HOST_USER,
    #             [owner.email],
    #             fail_silently= False,
    #             )
#post_save.connect(profileupdated, sender=Profile)
#post_delete.connect(profiledeleted, sender=Profile)