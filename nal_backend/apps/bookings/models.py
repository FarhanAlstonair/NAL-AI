import uuid
from django.db import models
from django.conf import settings

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]
    
    BOOKING_TYPE_CHOICES = [
        ('SITE_VISIT', 'Site Visit'),
        ('VIRTUAL_TOUR', 'Virtual Tour'),
        ('CONSULTATION', 'Consultation'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='bookings')
    
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default='SITE_VISIT')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    duration_minutes = models.IntegerField(default=60)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    
    # Contact details
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    
    # Virtual tour details
    virtual_tour_link = models.URLField(blank=True, null=True)
    virtual_tour_token = models.CharField(max_length=255, blank=True)
    
    # Cancellation
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['property']),
            models.Index(fields=['booking_date', 'booking_time']),
            models.Index(fields=['status']),
        ]

class BookingSlot(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='available_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    max_bookings = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'booking_slots'
        unique_together = ['property', 'date', 'start_time']