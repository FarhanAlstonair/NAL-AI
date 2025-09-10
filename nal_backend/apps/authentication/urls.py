from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='auth-login'),
    path('register/', views.register, name='auth-register'),
    path('refresh/', views.refresh_token, name='auth-refresh'),
    path('logout/', views.logout, name='auth-logout'),
]