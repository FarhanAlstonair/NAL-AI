from django.urls import path
from . import views

urlpatterns = [
    path('initiate/', views.initiate_payment, name='initiate-payment'),
    path('<uuid:transaction_id>/confirm/', views.confirm_payment, name='confirm-payment'),
    path('transactions/', views.list_transactions, name='list-transactions'),
    path('webhooks/razorpay/', views.webhook_handler, name='razorpay-webhook'),
]