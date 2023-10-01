from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import django.utils
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

status = (
    ('1', 'Under Review'),
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

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField('shortcut', blank=True)
    assign = models.ManyToManyField(User)
    efforts = models.DurationField(default=timedelta())
    status = models.CharField(max_length=7, choices=status, default=1)
    dead_line = models.DateField()
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE)
    complete_per = models.FloatField(max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True)
    add_date = models.DateField(auto_now_add=True)
    upd_date = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return (self.name)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assign = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    task_name = models.CharField(max_length=80)
    status = models.CharField(max_length=20, choices=status, default=1)
    due = models.CharField(max_length=7, choices=due, default=1)
    assDate = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    uoc = models.IntegerField(default=1)

    class Meta:
        ordering = ('project', 'task_name')

    def __str__(self):
        return(self.task_name)

class TaskTime(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    estimatedTime = models.CharField(max_length=100)
    userAddedTime = models.CharField(max_length=100)


class Issue(models.Model):
    name = models.CharField(max_length=30)
    descrip = models.CharField(max_length=100)
    assign = models.ForeignKey(User, on_delete=models.CASCADE)
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    board = models.CharField(max_length=20, choices=boards, default=1)
    creation = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    