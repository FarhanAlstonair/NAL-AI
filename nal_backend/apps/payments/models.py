import uuid
from django.db import models
from django.conf import settings

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]
    
    TRANSACTION_TYPE_CHOICES = [
        ('BOOKING_FEE', 'Booking Fee'),
        ('SECURITY_DEPOSIT', 'Security Deposit'),
        ('COMMISSION', 'Commission'),
        ('REFUND', 'Refund'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=5, default='INR')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Payment Gateway Integration
    payment_provider = models.CharField(max_length=50, default='razorpay')
    payment_intent_id = models.CharField(max_length=255, blank=True)
    payment_method_id = models.CharField(max_length=255, blank=True)
    gateway_transaction_id = models.CharField(max_length=255, blank=True)
    gateway_response = models.JSONField(default=dict)
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'transactions'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['property']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_intent_id']),
            models.Index(fields=['gateway_transaction_id']),
        ]

class PaymentMethod(models.Model):
    METHOD_TYPE_CHOICES = [
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('NET_BANKING', 'Net Banking'),
        ('WALLET', 'Digital Wallet'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=20, choices=METHOD_TYPE_CHOICES)
    provider_method_id = models.CharField(max_length=255)  # Gateway's method ID
    
    # Masked details for display
    display_name = models.CharField(max_length=100)  # e.g., "**** 1234"
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payment_methods'

class WebhookEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('PAYMENT_SUCCESS', 'Payment Success'),
        ('PAYMENT_FAILED', 'Payment Failed'),
        ('REFUND_PROCESSED', 'Refund Processed'),
    ]
    
    provider = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    event_id = models.CharField(max_length=255, unique=True)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'webhook_events'