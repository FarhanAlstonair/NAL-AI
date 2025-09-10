import uuid
from django.db import models
from django.conf import settings

class Document(models.Model):
    DOC_TYPE_CHOICES = [
        ('TITLE_DEED', 'Title Deed'),
        ('ENCUMBRANCE', 'Encumbrance Certificate'),
        ('TAX_RECEIPT', 'Tax Receipt'),
        ('IDENTITY', 'Identity Proof'),
        ('NOC', 'No Objection Certificate'),
        ('SURVEY', 'Survey Document'),
        ('APPROVAL', 'Approval Document'),
    ]
    
    STATUS_CHOICES = [
        ('UPLOADED', 'Uploaded'),
        ('PROCESSING', 'Processing'),
        ('VERIFIED', 'Verified'),
        ('PENDING', 'Pending Review'),
        ('REJECTED', 'Rejected'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    storage_key = models.CharField(max_length=500)  # S3 key
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPLOADED')
    verification_result = models.JSONField(default=dict)
    processed_text = models.TextField(blank=True)  # OCR extracted text
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'documents'
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['property']),
            models.Index(fields=['doc_type']),
            models.Index(fields=['status']),
        ]

class DocumentVerification(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='verifications')
    verifier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    audit_metadata = models.JSONField(default=dict)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'document_verifications'

class DocumentTemplate(models.Model):
    doc_type = models.CharField(max_length=20, unique=True)
    required_fields = models.JSONField(default=list)
    validation_rules = models.JSONField(default=dict)
    ml_model_config = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'document_templates'