from django import forms
from django.utils.text import slugify
from .models import Task
from .models import Project
from .models import Issue
from register.models import Company
from django.contrib.auth.models import User
from django.forms import ModelForm

status = (
    ('1', 'Stuck'),
    ('2', 'Working'),
    ('3', 'Done'),
)

due = (
    ('1', 'On Due'),
    ('2', 'Overdue'),
    ('3', 'Done'),
)

boards = (
    ('1', 'Upcoming'),
    ('2', 'In Progress'),
    ('3', 'On Hold'),
    ('4', 'Completed'),
)

class TaskEditForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class IssueForm(ModelForm):
    name = forms.CharField(max_length=80)
    descrip = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':5}))
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    assign = forms.ModelChoiceField(queryset=User.objects.all())
    board = forms.ChoiceField(choices=boards)
    deadline = forms.DateField()

    class Meta():
        model = Issue
        fields = '__all__'

    def save(self, commit=True):
        Issue = super(IssueForm, self).save(commit=False)
        Issue.name = self.cleaned_data['name']
        Issue.descrip = self.cleaned_data['descrip']
        Issue.project = self.cleaned_data['project']
        Issue.assign = self.cleaned_data['assign']
        Issue.board = self.cleaned_data['board']
        Issue.save()

        if commit:
            Issue.save()

        return Issue

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Issue Name'  
        self.fields['descrip'].widget.attrs['class'] = 'form-control'
        self.fields['descrip'].widget.attrs['placeholder'] = 'Issue Description'  
        self.fields['assign'].widget.attrs['class'] = 'form-control'
        self.fields['assign'].widget.attrs['placeholder'] = 'Assigned'  
        self.fields['project'].widget.attrs['class'] = 'form-control'
        self.fields['project'].widget.attrs['placeholder'] = 'Project'  
        self.fields['board'].widget.attrs['class'] = 'form-control'
        self.fields['board'].widget.attrs['placeholder'] = 'board'  
        self.fields['deadline'].widget.attrs['class'] = 'form-control'
        self.fields['deadline'].widget.attrs['placeholder'] = 'Deadline'              
        

class TaskRegistrationForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    assign = forms.ModelChoiceField(queryset=User.objects.all())
    task_name = forms.CharField(max_length=80)
    status = forms.ChoiceField(choices=status)
    due = forms.ChoiceField(choices=due)
    deadline = forms.DateField()
    assDate = forms.DateField()
    uoc = forms.CharField()

    class Meta:
        model = Task
        fields = '__all__'


    def save(self, commit=True):
        task = super(TaskRegistrationForm, self).save(commit=False)
        task.project = self.cleaned_data['project']
        task.task_name = self.cleaned_data['task_name']
        task.status = self.cleaned_data['status']
        task.due = self.cleaned_data['due']
        task.deadline = self.cleaned_data['deadline']
        task.assDate = self.cleaned_data['assDate']
        task.uoc = self.cleaned_data['uoc']
        assigns = self.cleaned_data['assign']
        task.save()

        if commit:
            task.save()

        return task


    def __init__(self, *args, **kwargs):
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['project'].widget.attrs['class'] = 'form-control'
        self.fields['project'].widget.attrs['placeholder'] = 'Social Name'
        self.fields['task_name'].widget.attrs['class'] = 'form-control'
        self.fields['task_name'].widget.attrs['placeholder'] = 'Name'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Email'
        self.fields['due'].widget.attrs['class'] = 'form-control'
        self.fields['due'].widget.attrs['placeholder'] = 'City'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
        self.fields['assign'].widget.attrs['placeholder'] = 'Found date'
        self.fields['deadline'].widget.attrs['class'] = 'form-control'
        self.fields['deadline'].widget.attrs['placeholder'] = 'Deadline'
        self.fields['assDate'].widget.attrs['class'] = 'form-control'
        self.fields['assDate'].widget.attrs['placeholder'] = 'Assigned On'
        self.fields['uoc'].widget.attrs['class'] = 'form-control'
        self.fields['uoc'].widget.attrs['placeholder'] = 'UOC'

class ProjectRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    # slug = forms.SlugField('shortcut')
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    efforts = forms.DurationField()
    status = forms.ChoiceField(choices=status)
    dead_line = forms.DateField()
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    complete_per = forms.FloatField(min_value=0, max_value=100)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Project
        fields = '__all__'


    def save(self, commit=True):
        Project = super(ProjectRegistrationForm, self).save(commit=False)
        Project.name = self.cleaned_data['name']
        Project.efforts = self.cleaned_data['efforts']
        Project.status = self.cleaned_data['status']
        Project.dead_line = self.cleaned_data['dead_line']
        Project.company = self.cleaned_data['company']
        Project.complete_per = self.cleaned_data['complete_per']
        Project.description = self.cleaned_data['description']
        Project.slug = slugify(str(self.cleaned_data['name']))
        Project.save()
        assigns = self.cleaned_data['assign']
        for assign in assigns:
            Project.assign.add((assign))

        if commit:
            Project.save()

        return Project


    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Project Name'
        self.fields['efforts'].widget.attrs['class'] = 'form-control'
        self.fields['efforts'].widget.attrs['placeholder'] = 'Efforts'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Status'
        self.fields['dead_line'].widget.attrs['class'] = 'form-control'
        self.fields['dead_line'].widget.attrs['placeholder'] = 'Dead Line, type a date'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        self.fields['company'].widget.attrs['placeholder'] = 'Company'
        self.fields['complete_per'].widget.attrs['class'] = 'form-control'
        self.fields['complete_per'].widget.attrs['placeholder'] = 'Complete %'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Type here the project description...'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
