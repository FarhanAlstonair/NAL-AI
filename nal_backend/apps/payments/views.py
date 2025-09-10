import hashlib
import hmac
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from .models import Transaction, WebhookEvent
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """Initiate payment process"""
    try:
        data = request.data
        required_fields = ['amount', 'transaction_type', 'property_id']
        
        if not all(field in data for field in required_fields):
            return Response({
                'success': False,
                'errors': [f'Required fields: {", ".join(required_fields)}']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create transaction record
        transaction = Transaction.objects.create(
            user=request.user,
            property_id=data['property_id'],
            amount=data['amount'],
            transaction_type=data['transaction_type'],
            description=data.get('description', ''),
            metadata=data.get('metadata', {})
        )
        
        # Simulate payment gateway integration (Razorpay)
        payment_intent = {
            'id': f'pi_{transaction.uuid}',
            'amount': int(float(data['amount']) * 100),  # Convert to paise
            'currency': 'INR',
            'status': 'requires_payment_method'
        }
        
        transaction.payment_intent_id = payment_intent['id']
        transaction.status = 'PROCESSING'
        transaction.save()
        
        return Response({
            'success': True,
            'data': {
                'transaction_id': transaction.uuid,
                'payment_intent': payment_intent,
                'client_secret': f'pi_{transaction.uuid}_secret_test'
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'errors': ['Failed to initiate payment']
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request, transaction_id):
    """Confirm payment completion"""
    try:
        transaction = Transaction.objects.get(uuid=transaction_id, user=request.user)
        
        payment_method_id = request.data.get('payment_method_id')
        if not payment_method_id:
            return Response({
                'success': False,
                'errors': ['payment_method_id is required']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Simulate payment processing
        # In production, integrate with actual payment gateway
        success = True  # Simulate success
        
        if success:
            transaction.status = 'COMPLETED'
            transaction.payment_method_id = payment_method_id
            transaction.gateway_transaction_id = f'txn_{transaction.uuid}'
            transaction.completed_at = timezone.now()
            transaction.gateway_response = {
                'status': 'success',
                'gateway_transaction_id': f'txn_{transaction.uuid}',
                'payment_method': payment_method_id
            }
        else:
            transaction.status = 'FAILED'
            transaction.gateway_response = {
                'status': 'failed',
                'error': 'Payment declined'
            }
        
        transaction.save()
        
        return Response({
            'success': True,
            'data': {
                'transaction_id': transaction.uuid,
                'status': transaction.status,
                'gateway_transaction_id': transaction.gateway_transaction_id
            }
        })
        
    except Transaction.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Transaction not found']
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transactions(request):
    """List user's transactions"""
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        transactions = transactions.filter(status=status_filter)
    
    # Filter by property
    property_id = request.GET.get('property_id')
    if property_id:
        transactions = transactions.filter(property__uuid=property_id)
    
    transaction_data = []
    for txn in transactions:
        transaction_data.append({
            'uuid': txn.uuid,
            'amount': txn.amount,
            'currency': txn.currency,
            'transaction_type': txn.transaction_type,
            'status': txn.status,
            'description': txn.description,
            'gateway_transaction_id': txn.gateway_transaction_id,
            'created_at': txn.created_at,
            'completed_at': txn.completed_at
        })
    
    return Response({
        'success': True,
        'data': transaction_data
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def webhook_handler(request):
    """Handle payment gateway webhooks"""
    try:
        # Verify webhook signature (implement based on your payment provider)
        signature = request.headers.get('X-Razorpay-Signature', '')
        payload = request.body
        
        # Verify signature (simplified - implement proper verification)
        # expected_signature = hmac.new(
        #     settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        #     payload,
        #     hashlib.sha256
        # ).hexdigest()
        
        # if not hmac.compare_digest(signature, expected_signature):
        #     return Response({'error': 'Invalid signature'}, status=400)
        
        event_data = json.loads(payload)
        event_type = event_data.get('event')
        
        # Create webhook event record
        webhook_event = WebhookEvent.objects.create(
            provider='razorpay',
            event_type=event_type,
            event_id=event_data.get('id', ''),
            payload=event_data
        )
        
        # Process webhook based on event type
        if event_type == 'payment.captured':
            payment_id = event_data['payload']['payment']['entity']['id']
            # Find and update transaction
            try:
                transaction = Transaction.objects.get(payment_intent_id=payment_id)
                transaction.status = 'COMPLETED'
                transaction.completed_at = timezone.now()
                transaction.save()
                
                webhook_event.transaction = transaction
                webhook_event.processed = True
                webhook_event.processed_at = timezone.now()
                webhook_event.save()
                
            except Transaction.DoesNotExist:
                pass
        
        elif event_type == 'payment.failed':
            payment_id = event_data['payload']['payment']['entity']['id']
            try:
                transaction = Transaction.objects.get(payment_intent_id=payment_id)
                transaction.status = 'FAILED'
                transaction.save()
                
                webhook_event.transaction = transaction
                webhook_event.processed = True
                webhook_event.processed_at = timezone.now()
                webhook_event.save()
                
            except Transaction.DoesNotExist:
                pass
        
        return Response({'status': 'success'})
        
    except Exception as e:
        return Response({
            'error': 'Webhook processing failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)