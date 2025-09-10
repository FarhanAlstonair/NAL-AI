import uuid
import boto3
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import Document, DocumentVerification
from .tasks import process_document_ocr

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_upload_url(request):
    """Generate presigned URL for document upload"""
    try:
        file_name = request.data.get('file_name')
        file_type = request.data.get('file_type')
        doc_type = request.data.get('doc_type')
        
        if not all([file_name, file_type, doc_type]):
            return Response({
                'success': False,
                'errors': ['file_name, file_type, and doc_type are required']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate unique storage key
        file_extension = file_name.split('.')[-1]
        storage_key = f"documents/{request.user.uuid}/{uuid.uuid4()}.{file_extension}"
        
        # Generate presigned URL
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': storage_key,
                'ContentType': file_type
            },
            ExpiresIn=3600
        )
        
        return Response({
            'success': True,
            'data': {
                'upload_url': presigned_url,
                'storage_key': storage_key,
                'expires_in': 3600
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'errors': ['Failed to generate upload URL']
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_document(request):
    """Create document record after successful upload"""
    try:
        data = request.data
        required_fields = ['title', 'doc_type', 'storage_key', 'file_size', 'mime_type']
        
        if not all(field in data for field in required_fields):
            return Response({
                'success': False,
                'errors': [f'Required fields: {", ".join(required_fields)}']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        document = Document.objects.create(
            owner=request.user,
            property_id=data.get('property_id'),
            title=data['title'],
            doc_type=data['doc_type'],
            storage_key=data['storage_key'],
            file_size=data['file_size'],
            mime_type=data['mime_type']
        )
        
        # Trigger async processing
        process_document_ocr.delay(document.id)
        
        return Response({
            'success': True,
            'data': {
                'document_id': document.uuid,
                'status': document.status,
                'message': 'Document uploaded successfully and processing started'
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'errors': ['Failed to create document record']
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_documents(request):
    """List user's documents"""
    documents = Document.objects.filter(owner=request.user).order_by('-created_at')
    
    # Filter by property if specified
    property_id = request.GET.get('property_id')
    if property_id:
        documents = documents.filter(property__uuid=property_id)
    
    # Filter by document type
    doc_type = request.GET.get('doc_type')
    if doc_type:
        documents = documents.filter(doc_type=doc_type)
    
    document_data = []
    for doc in documents:
        document_data.append({
            'uuid': doc.uuid,
            'title': doc.title,
            'doc_type': doc.doc_type,
            'status': doc.status,
            'file_size': doc.file_size,
            'mime_type': doc.mime_type,
            'verification_result': doc.verification_result,
            'created_at': doc.created_at,
            'updated_at': doc.updated_at
        })
    
    return Response({
        'success': True,
        'data': document_data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document(request, document_id):
    """Get document details with download URL"""
    try:
        document = Document.objects.get(uuid=document_id, owner=request.user)
        
        # Generate download URL
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        download_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': document.storage_key
            },
            ExpiresIn=3600
        )
        
        return Response({
            'success': True,
            'data': {
                'uuid': document.uuid,
                'title': document.title,
                'doc_type': document.doc_type,
                'status': document.status,
                'verification_result': document.verification_result,
                'processed_text': document.processed_text,
                'download_url': download_url,
                'created_at': document.created_at,
                'updated_at': document.updated_at
            }
        })
        
    except Document.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Document not found']
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_document(request, document_id):
    """Manual document verification (for verifiers)"""
    if request.user.role != 'VERIFIER':
        return Response({
            'success': False,
            'errors': ['Only verifiers can perform manual verification']
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        document = Document.objects.get(uuid=document_id)
        verification_status = request.data.get('status')
        notes = request.data.get('notes', '')
        
        if verification_status not in ['VERIFIED', 'REJECTED']:
            return Response({
                'success': False,
                'errors': ['Status must be VERIFIED or REJECTED']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update document status
        document.status = verification_status
        document.save()
        
        # Create verification record
        DocumentVerification.objects.create(
            document=document,
            verifier=request.user,
            status=verification_status,
            notes=notes,
            audit_metadata={'manual_verification': True}
        )
        
        return Response({
            'success': True,
            'data': {
                'message': f'Document {verification_status.lower()} successfully',
                'status': verification_status
            }
        })
        
    except Document.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Document not found']
        }, status=status.HTTP_404_NOT_FOUND)