from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.get_profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('<uuid:user_id>/', views.get_user_by_id, name='user-by-id'),
]