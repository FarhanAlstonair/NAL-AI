import uuid
from django.db import models
from django.conf import settings

class Property(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('UNDER_REVIEW', 'Under Review'),
        ('ARCHIVED', 'Archived'),
        ('SOLD', 'Sold'),
    ]
    
    PROPERTY_TYPE_CHOICES = [
        ('APARTMENT', 'Apartment'),
        ('HOUSE', 'House'),
        ('VILLA', 'Villa'),
        ('PLOT', 'Plot'),
        ('COMMERCIAL', 'Commercial'),
        ('WAREHOUSE', 'Warehouse'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_properties')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_properties')
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=5, default='INR')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT')
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Property Details
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    area_sqft = models.IntegerField(null=True, blank=True)
    parking_spaces = models.IntegerField(default=0)
    
    # Scoring & Valuation
    ribl_score = models.FloatField(null=True, blank=True)
    urgent_sale_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'properties'
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['agent']),
            models.Index(fields=['price']),
            models.Index(fields=['property_type']),
            models.Index(fields=['status']),
            models.Index(fields=['city', 'state']),
        ]

class PropertyMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('VIRTUAL_TOUR', 'Virtual Tour'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='media')
    media_url = models.URLField()
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='IMAGE')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'property_media'

class PropertyAmenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'property_amenities'
        verbose_name_plural = 'Property Amenities'

class PropertyAmenityMapping(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    amenity = models.ForeignKey(PropertyAmenity, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'property_amenity_mapping'
        unique_together = ['property', 'amenity']