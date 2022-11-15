import profile
from django.shortcuts import render , redirect
from .utils import searchProjects
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import *
# Create your views here.





def projects(request):
    
    projects , search_query = searchProjects(request)
    projects , custom_range = paginateProjects(request,projects,6)
    
    ctx = {'projects':projects, 'search_query':search_query,
        'custom_range':custom_range}
    return render(request, 'projects/projects.html',ctx)


def project(request,pk):
    projectobj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectobj
        review.owner = request.user.profile
        review.save()

        projectobj.getVoteCount
        
        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectobj.id)

    return render(request, 'projects/single_project.html', {'projectobj': projectobj, 'form': form})


@login_required(login_url="login")
def editProject(request,pk):
    profile = request.user.profile
    projectobj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectobj)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES,instance=projectobj)
        if form.is_valid():
            form.save()
            return redirect('projects')
    ctx = {'projectobj':projectobj,'form':form,}
    return render(request, 'projects/project_form.html',ctx)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False) 
            project.owner = profile
            project.save()        
            messages.success(request, 'project added successfully!')
            return redirect('projects')
    ctx = {'form':form,}
    return render(request, 'projects/project_form.html',ctx)



@login_required(login_url="login")
def delProject(request,pk):
    profile = request.user.profile
    projectobj = profile.project_set.get(id=pk)
    if request.method == 'POST':
        projectobj.delete()
        return redirect('projects')
    ctx = {'object':projectobj}
    return render(request, 'delete_confirm.html',ctx)


