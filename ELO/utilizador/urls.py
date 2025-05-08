from django.urls import path
from . import views
from .views import criar_conta_view
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

urlpatterns = [
    path('', views.home, name='homepage'),
    path('register/', criar_conta_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   # path('recuperar-password/', auth_views.PasswordResetView.as_view(template_name='utilizador/password_reset.html'), name='password_reset'),
    path('recuperar-password/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='utilizador/password_reset_done.html'), name='password_reset_done'),
    path('recuperar-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='utilizador/password_reset_confirm.html'), name='password_reset_confirm'),
    path('recuperar-password/feito/', auth_views.PasswordResetCompleteView.as_view(template_name='utilizador/password_reset_complete.html'), name='password_reset_complete'),
    path('recuperar-password/', CustomPasswordResetView.as_view(), name='password_reset'),


]
