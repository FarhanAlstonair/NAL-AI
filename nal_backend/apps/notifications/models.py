import uuid
from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = [
        ('BOOKING_CONFIRMED', 'Booking Confirmed'),
        ('PAYMENT_SUCCESS', 'Payment Success'),
        ('DOCUMENT_VERIFIED', 'Document Verified'),
        ('PROPERTY_APPROVED', 'Property Approved'),
        ('MESSAGE_RECEIVED', 'Message Received'),
    ]
    
    CHANNEL_CHOICES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push Notification'),
        ('WHATSAPP', 'WhatsApp'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
    ]
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    payload = models.JSONField(default=dict)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['type', 'channel']),
        ]