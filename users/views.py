import re
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  , login , logout
from users.models import Profile , Skill, Message
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .utils import *



def profiles(request):
    profiles , search_query = searchProfiles(request)
    profiles , custom_range = paginateProfiles(request,profiles,6)

    ctx = {'profiles':profiles,
        'custom_range':custom_range ,'search_query':search_query}
    return render(request, 'users/profiles.html',ctx)



def userProfile(request,pk):
    profileobj = Profile.objects.get(id=pk)
    projects = profileobj.project_set.all()
    skills = profileobj.skill_set.all()
    topskills = skills.exclude(description="")
    otherskills = skills.filter(description="")
    ctx = {'profile':profileobj,'topskills':topskills,
        'otherskills':otherskills,'projects':projects}
    return render(request, 'users/profile.html',ctx)



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        try:
            return redirect(request.GET.get("next"))
        except:
            return redirect('profiles')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'username does not exist!')
        

        user = authenticate(request, username = username , password = password)
        if user != None:
            login(request, user)
            try:
                return redirect(request.GET.get("next", None))
            except:
                return redirect('profiles')
        else:
            messages.error(request, 'username or password is incorrect!')    
            
    return render(request, 'users/login_register.html',{'page':page})


def logoutUser(request):
    logout(request)
    messages.success(request, 'user logged out!')    
    return redirect('login')



def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"user created!")
            return redirect('profiles')
    return render(request, 'users/login_register.html',{'page':page,'form':form})



@login_required(login_url='login')
def userAccount(request):
    user = request.user
    profile = user.profile
    ctx = {'profile':profile}
    return render(request, 'users/account.html', ctx)


@login_required(login_url="login")
def addSkill(request):
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()            
            messages.success(request,'skill added successfully!')
            return redirect('account')
    ctx = {'form':form}
    return render(request, 'users/skill_form.html',ctx)


@login_required(login_url="login")
def editSkill(request,pk):
    skill = request.user.profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            skill.owner = request.user.profile
            skill.save()            
            messages.success(request,'skill updated successfully!')
            return redirect('account')
    ctx = {'form':form}
    return render(request, 'users/skill_form.html',ctx)


@login_required(login_url="login")
def deleteSkill(request,pk):
    skill = request.user.profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request,'skill deleted successfully!')
        return redirect('account')
    object = skill.name
    ctx = {'object':object}
    return render(request, 'delete_confirm.html',ctx)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully!')
            return redirect('account')
    ctx = {'form':form}
    return render(request,'users/profile_form.html',ctx)




@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)



@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)




def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
        
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)