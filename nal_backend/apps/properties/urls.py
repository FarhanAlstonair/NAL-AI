from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_properties, name='list-properties'),
    path('create/', views.create_property, name='create-property'),
    path('<uuid:property_id>/', views.get_property, name='get-property'),
    path('<uuid:property_id>/update/', views.update_property, name='update-property'),
    path('<uuid:property_id>/media/', views.upload_property_media, name='upload-property-media'),
]