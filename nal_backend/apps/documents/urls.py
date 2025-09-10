from django.urls import path
from . import views

urlpatterns = [
    path('upload-url/', views.get_upload_url, name='get-upload-url'),
    path('create/', views.create_document, name='create-document'),
    path('', views.list_documents, name='list-documents'),
    path('<uuid:document_id>/', views.get_document, name='get-document'),
    path('<uuid:document_id>/verify/', views.verify_document, name='verify-document'),
]