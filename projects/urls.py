from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('new-project/', views.newProject, name='new-project'),
    path('new-task/', views.newTask, name='new-task'),
    path('mytasks/', views.tasksDetails, name='tasksDetails'),
    path('myissue/', views.issueDetails, name='issueDetails'),
    path('mytasks/<taskId>/', views.change_status, name='change_status'),
    path('mytasks/<id>/<status>', views.reject_review, name='reject_review'),
    path('kanban/<id>/<boardno>',views.boardupdate, name='boardupdate'),

]
