from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<id>/', views.genreport, name='genreport'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('churn/', views.churn, name='churn'),
    path('appraisal/',views.appraisal, name='appraisal'),
    path('selfeval/',views.selfeval, name='selfeval'),
    path('gantt/',views.ganttview, name='ganttview'),
    path('gantt/<id>/',views.ganttfilter, name='ganttfilter'),
    path('empdash/',views.empdash, name='empdash'),
    path('kanban/',views.kanban, name='kanban'),
    path('kanban/<id>/<boardno>',views.boardupdate, name='boardupdate'),
    path('kanban/<id>/',views.filterboard, name='filterboard'),
    path('ganttinsert/',views.ganttinsert, name='ganttinsert'),
    path('chat/',views.chat, name='chat'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
