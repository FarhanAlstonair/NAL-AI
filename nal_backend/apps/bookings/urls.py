from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create-booking'),
    path('', views.list_bookings, name='list-bookings'),
    path('<uuid:booking_id>/', views.get_booking, name='get-booking'),
    path('<uuid:booking_id>/status/', views.update_booking_status, name='update-booking-status'),
    path('slots/<uuid:property_id>/', views.get_available_slots, name='get-available-slots'),
]