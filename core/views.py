from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect
from register.models import Company
from register.models import Project
from register.models import UserProfile, EmpProfile
from projects.models import Task, Issue

from register.forms import EmpAppraisalForm, SelfEvalForm
from projects.forms import IssueForm

from django.http import HttpResponse, JsonResponse

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from fpdf import FPDF
import joblib

import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.offline import plot
from plotly.graph_objs import Scatter

import datetime
import sklearn
import pandas as pd
import numpy as np
import csv
import json

pdf = FPDF('P','mm','Letter')

le = LabelEncoder()

def chat(request):
    return render(request,'core/chat.html')

def kanban(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        context = {'form': form}
        print(form)
        if form.is_valid():
            form.save()
            created = True
            form = IssueForm()
            upcoming = Issue.objects.all().filter(board=1)
            inprogress = Issue.objects.all().filter(board=2)
            onhold = Issue.objects.all().filter(board=3)
            completed = Issue.objects.all().filter(board=4)
            project = Project.objects.all()
            user = UserProfile.objects.all()

            context = {
                'created': created,
                'form': form,
                'upcoming':upcoming,
                'inprogress':inprogress,
                'onhold':onhold,
                'completed':completed,
                'project':project,
                'users':user
            }
            return redirect('core:kanban')
        else:
            return render(request, 'core/kanban.html', context)
    else:
        upcoming = Issue.objects.all().filter(board=1)
        inprogress = Issue.objects.all().filter(board=2)
        onhold = Issue.objects.all().filter(board=3)
        completed = Issue.objects.all().filter(board=4)
        project = Project.objects.all()
        user = UserProfile.objects.all()

        form = IssueForm()
        context = {
            'form': form,
            'upcoming':upcoming,
            'inprogress':inprogress,
            'onhold':onhold,
            'completed':completed,
            'project':project,
            'users':user
        }
        return render(request,'core/kanban.html', context)

def filterboard(request,id):
    upcoming = Issue.objects.all().filter(board=1).filter(project=id)
    inprogress = Issue.objects.all().filter(board=2).filter(project=id)
    onhold = Issue.objects.all().filter(board=3).filter(project=id)
    completed = Issue.objects.all().filter(board=4).filter(project=id)
    project = Project.objects.all()
    user = UserProfile.objects.all()
    form = IssueForm()
    context = {
        'form': form,
        'upcoming':upcoming,
        'inprogress':inprogress,
        'onhold':onhold,
        'completed':completed,
        'project':project,
        'users':user
    }
    return render(request,'core/kanban.html', context)

def boardupdate(request,id,boardno):
    issue = Issue.objects.get(id=id)
    issue.board = boardno
    issue.save()
    return redirect('core:kanban')

def ganttinsert(request):
    new = request.POST['data']
    newTask = json.loads(new)
    print(newTask)
    as1 = {
        'Success':True
    }
    p = Project.objects.get(id=1)
    t = Task(
        project=p,
        task_name=newTask['text'],
        status=2,
        assDate="2021-03-05",
        deadline="2021-04-10"
    )
    t.save()
    print(t)
    return JsonResponse(as1)

def ganttfilter(request,id):
    tasks = Task.objects.all().filter(project=id)
    projects = Project.objects.all()
    context = {
        'tasks':tasks,
        'project':projects,
    }
    for t in tasks:
        print(t.project.id,"Name: ", t.project)
    return render(request, 'core/gantt.html', context)

def ganttview(request):
    tasks = Task.objects.all()
    projects = Project.objects.all()
    context = {
        'tasks':tasks,
        'project':projects,
    }
    for t in tasks:
        print(t.project.id,"Name: ", t.project)
    return render(request, 'core/gantt.html', context)

def empdash(request):
    curr_user = request.user
    user = UserProfile.objects.get(user=curr_user)
    tasks = Task.objects.filter(assign=curr_user.id)
    project = Project.objects.get(assign=curr_user.id)
    issue = Issue.objects.filter(assign=curr_user.id)

    team = Project.objects.get(name=project.name)
    team = team.assign.all()

    overdue = tasks.filter(due=2).count()
    print(overdue)

    ttlTask = Task.objects.all().filter(project=project.id).count()
    print(ttlTask)

    context = {
        "curr_user":curr_user,
        "tasks":tasks,
        "project":project,
        'profile':user,
        'team': team,
        'issue':issue,
        'total':ttlTask,
    }
    return render(request, 'core/empdash.html', context)

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def selfeval(request):
    active_users = User.objects.all().filter(is_active=True)
    if request.method == 'POST':
        form = SelfEvalForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()

            technical_skills = int(request.POST['technical_skills'])
            technical_knowledge =  int(request.POST['technical_knowledge'])
            quality_of_work = int(request.POST['quality_of_work'])
            productivity = int(request.POST['productivity'])
            project_management_skills = int(request.POST['project_management_skills'])
            technology_skills = int(request.POST['technology_skills'])
            time_management = int(request.POST['time_management'])
            interpersonal_skills = int(request.POST['interpersonal_skills'])
            communication_skills = int(request.POST['communication_skills'])
            innovation = int(request.POST['innovation'])
            collaboration = int(request.POST['collaboration'])
            employee_policies = int(request.POST['employee_policies'])
            leadership_skills = int(request.POST['leadership_skills'])
            professionalism = int(request.POST['professionalism'])

            sum1 = (technical_skills + technical_knowledge +quality_of_work+productivity+project_management_skills+technology_skills+time_management+interpersonal_skills+communication_skills+innovation+collaboration+employee_policies+leadership_skills+professionalism)/70
            
            ep = EmpProfile.objects.get(emp=equest.user)
            print(ep.satisfaction_level)
            ep.satisfaction_level = sum1
            ep.save()
            print(ep.satisfaction_level)

            created = True
            form = SelfEvalForm()
            context = {
                'created': created,
                'form': form,
                'active_users':active_users,
            }
            return render(request, 'core/selfeval.html', context)
        else:
            return render(request, 'core/selfeval.html', context)
    else:
        form = SelfEvalForm()
        context = {
            'form': form,
            'active_users':active_users
        }
        return render(request, 'core/selfeval.html', context)
    
def dashboard(request):
    users = User.objects.all()
    active_users = User.objects.all().filter(is_active=True)
    companies = Company.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    under_review = Task.objects.all().filter(status=1).count()
    working = Task.objects.all().filter(status=2).count()
    done = Task.objects.all().filter(status=3).count()

    issue = Issue.objects.all()
    backlog = Issue.objects.all().filter(board=1).count()
    inprogress = Issue.objects.all().filter(board=2).count()
    onhold = Issue.objects.all().filter(board=3).count()
    completed = Issue.objects.all().filter(board=4).count()

    labels = ['Under Review','Working','Done']
    values = [under_review, working, done]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',title='Tasks Overview')])
    fig.update_traces(textfont_size=18)
    pie = plot(fig, output_type='div')

    labels = ['Backlog','In Progress','On Hold','Completed']
    values = [backlog, inprogress, onhold, completed]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',title='Issues Overview')])
    fig.update_traces(textfont_size=18)
    pieIss = plot(fig, output_type='div')

    labels = []
    for i in projects:
        labels.append(i.name)

    projects = Project.objects.all()
    count = []
    for i in projects:
        tas = Task.objects.filter(project=i.id)
        uocProject = 0
        for t in tas:
            uocProject = uocProject + t.uoc
        count.append(uocProject*2000)
    fig = go.Figure([go.Bar(x=labels, y=count),go.Bar(x=labels, y=count)])
    bar = plot(fig, output_type='div')

    context = {
        'users' : users,
        'active_users' : active_users,
        'companies' : companies,
        'projects' : projects,
        'tasks' : tasks,
        'pie':pie,
        'pieIss':pieIss,
    }
    return render(request, 'core/dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            return redirect('core:index')
        else:
            return render(request, 'register/login.html', {'login_form':form})
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'login_form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:index'))

def context(request):
    # send context to base.html
    # if not request.session.session_key:
    #     request.session.create()
    users = User.objects.all()
    users_prof = UserProfile.objects.all()
    if request.user.is_authenticated:
        try:
            users_prof = UserProfile.objects.exclude(
            id=request.user.userprofile_set.values_list()[0][0])  # exclude himself from invite list
            user_id = request.user.userprofile_set.values_list()[0][0]
            logged_user = UserProfile.objects.get(id=user_id)
            friends = logged_user.friends.all()
            context = {
                'users': users,
                'users_prof': users_prof,
                'logged_user': logged_user,
                'friends' : friends,
            }
            return context
        except:
            users_prof = UserProfile.objects.all()
            context = {
                'users':users,
                'users_prof':users_prof,
            }
            return context
    else:
        context = {
            'users': users,
            'users_prof': users_prof,
        }
        return context

def churn1(request):
    if request.method == 'POST':
        gb = joblib.load('final.sav')
        li = []
        li.append(request.POST['satisfaction_level'])
        li.append(request.POST['last_evaluation'])
        li.append(request.POST['number_project'])
        li.append(request.POST['avg_monthly_hours'])
        li.append(request.POST['time_spent'])
        li.append(request.POST['work_accident'])
        li.append(request.POST['promotion'])
        li.append(request.POST['departments'])
        li.append(request.POST['salary'])
        ans = gb.predict([li])
        if ans==0:
            res = "A 97% chance employee will not leave"
        else:
            res = "A 97% chance employee will leave"
        context = {
            'res': res,
        }
    else:
        context ={
            'res': ""
        }
    return render(request, 'core/churn.html', context)

def appraisal(request):
    if request.method == 'POST':
        print(request)
        form = EmpAppraisalForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            job = int(request.POST['job'])
            attend = int(request.POST['attend'])
            commu = int(request.POST['commu'])
            attitude = int(request.POST['attitude'])
            
            group_work = int(request.POST['group_work'])
            creativity = int(request.POST['creativity'])
            dependibility = int(request.POST['dependibility'])
            coworker_relations = int(request.POST['coworker_relations'])
            independent_work = int(request.POST['independent_work'])

            sum1 = job+attend+commu+attitude+group_work+creativity+dependibility+coworker_relations+independent_work

            ep = EmpProfile.objects.get(emp=request.POST['emp'])
            print(ep.last_evaluation)
            ep.last_evaluation = 0.94
            print(ep.last_evaluation)
            ep.save()

            created = True
            form = EmpAppraisalForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'core/appraisal.html', context)
        else:
            return render(request, 'core/appraisal.html', context)
    else:
        form = EmpAppraisalForm()
        context = {
            'form': form,
        }
        return render(request, 'core/appraisal.html', context)
    #users = User.objects.all()
    #active_users = User.objects.all().filter(is_active=True)
    #print(active_users)
    #UserP = UserProfile.objects.all()
    #context = {
        #'userP':UserP,
        #'users':users,
        #'active_users':active_users
    #}
    return render(request, 'core/appraisal.html', context)

def churn(request):

    df = pd.DataFrame(list(EmpProfile.objects.all().values()), columns=['satisfaction_level', 'last_evaluation', 'num_projects','avg_monthly_hrs', 'time_spent_company', 'work_accident','promotion_last_5_years', 'departments', 'salary_level'])
    #print(df)

    e = EmpProfile.objects.all()
    ids = []
    for i in e:
        ids.append(i.emp.first_name +" "+ i.emp.last_name)

    gb = joblib.load('RandomForrest.sav')
    
    test = df[['satisfaction_level', 'last_evaluation', 'num_projects','avg_monthly_hrs', 'time_spent_company', 'work_accident','promotion_last_5_years', 'departments', 'salary_level']]
    res = gb.predict(test)
    test.insert(9,"Result",res)
    test.insert(0,"Employee",ids)

    test = test[['Employee','satisfaction_level', 'last_evaluation', 'num_projects','avg_monthly_hrs', 'time_spent_company', 'departments', 'salary_level','Result']]
    ms = test["Result"] == 1
    pas = test[ms]

    atRiskList = pas['Employee']
    #print(atRiskList)

    pas = pas[['Employee','satisfaction_level', 'last_evaluation', 'num_projects','avg_monthly_hrs', 'time_spent_company', 'departments', 'salary_level']]
    pas = pas.rename(columns={
        'satisfaction_level':'Satisfaction Score',
        'last_evaluation':'Last Evaluation',
        'num_projects':'No. of Project',
        'avg_monthly_hrs':'Average Monthly Hours',
        'time_spent_company': 'Time Spent',
        'departments': 'Departments',
        'salary_level':'Salary Level',
    })
    data1 = pd.DataFrame(pas)
    df11 = pd.DataFrame(pas)
    df11['Salary Level'].replace('1', 'Low', inplace=True)
    df11['Salary Level'].replace('2', 'Medium', inplace=True)
    df11['Salary Level'].replace('3', 'High', inplace=True)
    df11['Departments'].replace("0","IT", inplace=True)
    df11['Departments'].replace("1","R&D", inplace=True)
    df11['Departments'].replace("2","Accounting", inplace=True)
    df11['Departments'].replace("3","HR", inplace=True)
    df11['Departments'].replace("4","Management", inplace=True)
    df11['Departments'].replace("5","Marketing", inplace=True)
    df11['Departments'].replace("6","Product Management", inplace=True)
    df11['Departments'].replace("7","Sales", inplace=True)
    df11['Departments'].replace("8","Support", inplace=True)
    df11['Departments'].replace("9","Technical", inplace=True)
    html = df11.to_html(classes='table table-striped',index=False)

    data1 = pd.DataFrame(pas)

    #Department Bar Graph
    data = [['IT', (data1['Departments']=='IT').sum()],
            ['RanD', (data1['Departments']=='R').sum()],
            ['Accounting', (data1['Departments']=='Accounting').sum()],
            ['HR', (data1['Departments']=='HR').sum()],
            ['Management', (data1['Departments']=='Management').sum()],
            ['Marketing', (data1['Departments']=='Marketing').sum()],
            ['Product Management', (data1['Departments']=='Product Management').sum()],
            ['Sales', (data1['Departments']=='Sales').sum()],
            ['Support', (data1['Departments']=='Support').sum()],
            ['Technical', (data1['Departments']=='Technical').sum()]]
    df = pd.DataFrame(data, columns=['Departments','Count'])
    #print(df)
    fig = px.bar(df, x='Departments',y='Count')
    depart_grap = plot(fig, output_type='div')

    data = [['Low', (data1['Salary Level']=='Low').sum()],
            ['Medium', (data1['Salary Level']=='Medium').sum()],
            ['High', (data1['Salary Level']=='High').sum()]]

    df = pd.DataFrame(data, columns=['Salary','Count'])
    fig = px.bar(df, x='Salary',y='Count')
    sal_grap = plot(fig, output_type='div')

    #Gender Diagram
    genderDF = UserProfile.objects.all()
    mC = UserProfile.objects.all().filter(gender='M').count()
    fC = UserProfile.objects.all().filter(gender='F').count()
    val = [mC,fC]
    #print(genderDF)
    fig = go.Figure(data=[go.Pie(labels=['Male','Female'], values=val, textinfo='label+percent',title='Gender Overview')])
    fig.update_traces(textfont_size=18)
    pie = plot(fig, output_type='div')


    context ={
        'data': html,
        'departG': depart_grap,
        'salG':sal_grap,
        'genderG': pie,

    }
    return render(request, 'core/churn.html', context)

def genreport(request,id):
    tasks = Task.objects.all().filter(project=id)
    issue = Issue.objects.all().filter(project=id)
    #print(issue)
    for t in tasks:
        name = str(t.project)

    p = Project.objects.get(name=name)
    summ = str(p.description)

    data = []
    for t in tasks:
        a = []
        a.append(t.task_name)
        a.append(t.assign)
        if t.due == 1:
            a.append("On Time")
        elif t.due == 2:
            a.append("Due")
        else:
            a.append("Done")
        a.append(t.deadline)
        data.append(a)
        a = []

    dataIssue = []
    for t in issue:
        a = []
        a.append(t.name)
        a.append(t.assign)
        if t.board == 1:
            a.append("Backlog")
        elif t.board == 2:
            a.append("In Progress")
        elif t.board == 3 :
            a.append("On Hold")
        else:
            a.append("Completed")
        dataIssue.append(a)
        a = []

    #print(dataIssue)
    create_report(name,summ,data,dataIssue)
    #print("Name:", name ,"\nDesp:",summ, "Data: ", data)
    return redirect('core:dashboard')

def create_report(name,summ,data,dataIssue):

    pdf.add_page()
    pdf.set_font('Arial','B',16)
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size

    pdf.ln(20)
    pdf.cell(0,17, f'Project Report',1,2,'C',)
    pdf.cell(45,15, f'Project Name: ',1,0,'L')
    pdf.set_font('Arial','',13)
    pdf.cell(0,15,name,1,1,'L')
    pdf.set_font('Arial','B',16)
    pdf.cell(0,15, f'Project Summary: ',1,2,'L')
    pdf.set_font('Arial','',13)
    pdf.multi_cell(0,10,summ,1,'L')
    pdf.ln(5)
    pdf.set_font('Arial','B',16)
    pdf.cell(50, 10, f'Project Overview',0,1)
    pdf.ln(5)

    headers = [['Task Name','Employee','Status','Deadline']]
    pdf.ln(0.5)
    # Here we add more padding by passing 2*th as height
    for row in headers:
        for datum in row:
            # Enter data in colums
            pdf.cell(col_width, 2*th, str(datum), border=1)

        pdf.ln(2*th)
    pdf.set_font('Arial','',13)
    for row in data:
        for datum in row:
            # Enter data in colums
            pdf.cell(col_width, 2*th, str(datum), border=1)

        pdf.ln(2*th)

    pdf.set_font('Arial','B',16)
    pdf.cell(50, 10, f'Issues Overview',0,1)
    pdf.ln(5)

    headers = [['Issue Name','Employee','Status']]
    pdf.ln(0.5)
    # Here we add more padding by passing 2*th as height
    for row in headers:
        for datum in row:
            # Enter data in colums
            pdf.cell(col_width, 2*th, str(datum), border=1)

        pdf.ln(2*th)
    pdf.set_font('Arial','',13)
    for row in dataIssue:
        for datum in row:
            # Enter data in colums
            pdf.cell(col_width, 2*th, str(datum), border=1)

        pdf.ln(2*th)
    op = name +".pdf"
    pdf.output(op,'F')
