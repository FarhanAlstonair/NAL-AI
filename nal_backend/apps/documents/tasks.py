from celery import shared_task
from django.conf import settings
import boto3
import json
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_document_ocr(document_id):
    """Process document OCR extraction"""
    from .models import Document
    
    try:
        document = Document.objects.get(id=document_id)
        document.status = 'PROCESSING'
        document.save()
        
        # Simulate OCR processing (replace with actual OCR service)
        extracted_text = f"Extracted text from {document.title}"
        
        # Update document with extracted text
        document.processed_text = extracted_text
        document.status = 'PENDING'
        document.save()
        
        # Trigger ML verification
        verify_document_ml.delay(document_id)
        
        logger.info(f"OCR processing completed for document {document_id}")
        
    except Document.DoesNotExist:
        logger.error(f"Document {document_id} not found")
    except Exception as e:
        logger.error(f"OCR processing failed for document {document_id}: {str(e)}")
        Document.objects.filter(id=document_id).update(status='REJECTED')

@shared_task
def verify_document_ml(document_id):
    """ML-based document verification"""
    from .models import Document, DocumentVerification
    
    try:
        document = Document.objects.get(id=document_id)
        
        # Simulate ML verification (replace with actual ML service)
        confidence_score = 0.85
        is_valid = confidence_score > 0.8
        
        verification_result = {
            'confidence_score': confidence_score,
            'is_valid': is_valid,
            'extracted_fields': {
                'document_number': 'DOC123456',
                'issue_date': '2023-01-01',
                'validity': '2025-01-01'
            },
            'anomalies': []
        }
        
        document.verification_result = verification_result
        
        if is_valid:
            document.status = 'VERIFIED'
        else:
            document.status = 'PENDING'  # Requires human review
        
        document.save()
        
        # Create verification record
        DocumentVerification.objects.create(
            document=document,
            status='VERIFIED' if is_valid else 'PENDING',
            audit_metadata=verification_result
        )
        
        logger.info(f"ML verification completed for document {document_id}")
        
    except Document.DoesNotExist:
        logger.error(f"Document {document_id} not found")
    except Exception as e:
        logger.error(f"ML verification failed for document {document_id}: {str(e)}")

@shared_task
def generate_presigned_url(storage_key, expiration=3600):
    """Generate presigned URL for S3 object"""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': storage_key},
            ExpiresIn=expiration
        )
        
        return url
        
    except Exception as e:
        logger.error(f"Failed to generate presigned URL for {storage_key}: {str(e)}")
        return None