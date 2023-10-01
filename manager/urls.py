from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth import views as av

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('register.urls', namespace='register')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('plotly/', include('django_plotly_dash.urls', namespace='plotly')),
    path('', include('core.urls', namespace='core')),

    path('password_reset/',av.PasswordResetView.as_view(template_name="register/reset_pass.html"), name='password_reset'),
    path('password_reset_sent/',av.PasswordResetDoneView.as_view(template_name="register/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',av.PasswordResetConfirmView.as_view(template_name="register/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete/',av.PasswordResetCompleteView.as_view(template_name="register/password_reset_complete.html"), name='password_reset_complete'),

    path('change_password/',av.PasswordChangeView.as_view(template_name="register/change_password.html"), name='change_password'),
    path('password_change_done', av.PasswordChangeDoneView.as_view(template_name="register/password_change_done.html"), name="password_change_done"),
]
