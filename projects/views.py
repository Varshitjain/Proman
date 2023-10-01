from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Avg
from register.models import Project
from projects.models import Task, Issue
from projects.forms import TaskRegistrationForm
from projects.forms import ProjectRegistrationForm
from projects.forms import TaskEditForm
from register.models import UserProfile, EmpProfile


def projects(request):
    projects = Project.objects.all()
    avg_projects = Project.objects.all().aggregate(Avg('complete_per'))['complete_per__avg']
    tasks = Task.objects.all()
    overdue_tasks = tasks.filter(due='2')
    context = {
        'avg_projects' : avg_projects,
        'projects' : projects,
        'tasks' : tasks,
        'overdue_tasks' : overdue_tasks,
    }
    return render(request, 'projects/projects.html', context)

def boardupdate(request,id,boardno):
    issue = Issue.objects.get(id=id)
    issue.board = boardno
    issue.save()
    return redirect('projects:issueDetails')

def newTask(request):
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_task.html', context)
        else:
            return render(request, 'projects/new_task.html', context)
    else:
        form = TaskRegistrationForm()
        context = {
            'form': form,
        }
        return render(request,'projects/new_task.html', context)

def newProject(request):
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = ProjectRegistrationForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_project.html', context)
        else:
            return render(request, 'projects/new_project.html', context)
    else:
        form = ProjectRegistrationForm()
        context = {
            'form': form,
        }
        return render(request,'projects/new_project.html', context)

def tasksDetails(request):
    curr_user = request.user
    if curr_user.is_staff:
        tasks = Task.objects.filter(status=1)
        context = {
            "curr_user":curr_user,
            "tasks":tasks,
        }
    else:
        tasks = Task.objects.filter(assign=curr_user.id)
        context = {
            "curr_user":curr_user,
            "tasks":tasks,
        }
    return render(request, 'projects/task_details.html',context)

def issueDetails(request):
    curr_user = request.user
    issue = Issue.objects.all().filter(assign=curr_user.id)
    upcoming = issue.filter(board=1)
    inprogress = issue.filter(board=2)
    onhold = issue.filter(board=3)
    completed = issue.filter(board=4)
    project = Project.objects.all()
    user = UserProfile.objects.all()
    context = {
        'upcoming':upcoming,
        'inprogress':inprogress,
        'onhold':onhold,
        'completed':completed,
        'project':project,
        'users':user
    }
    return render(request, 'projects/issue_details.html',context)


def change_status(request, taskId):
    curr_user = request.user
    if curr_user.is_staff:
        tasks = Task.objects.get(id=taskId)
        tasks.status = 3
        tasks.save()
        tasks = Task.objects.filter(status=1)
        context = {
            "curr_user":curr_user,
            "tasks":tasks,
        }
        return render(request, 'projects/task_details.html',context)
    else:
        tasks = Task.objects.get(id=taskId)
        tasks.status = 1
        tasks.save()
        tasks = Task.objects.filter(assign=curr_user.id)
        context = {
            "curr_user":curr_user,
            "tasks":tasks,
        }
        return render(request, 'projects/task_details.html',context)

def reject_review(request, id, status):
    curr_user = request.user
    tasks = Task.objects.get(id=id)
    print(tasks)
    tasks.status = 2
    tasks.save()
    tasks = Task.objects.filter(status=1)
    context = {
        "curr_user":curr_user,
        "tasks":tasks,
    }
    return render(request, 'projects/task_details.html',context)


    
