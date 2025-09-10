import uuid
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Booking, BookingSlot

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    """Create a new booking"""
    try:
        data = request.data
        required_fields = ['property_id', 'booking_date', 'booking_time', 'contact_name', 'contact_phone']
        
        if not all(field in data for field in required_fields):
            return Response({
                'success': False,
                'errors': [f'Required fields: {", ".join(required_fields)}']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate booking date (not in the past)
        booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
        if booking_date < timezone.now().date():
            return Response({
                'success': False,
                'errors': ['Booking date cannot be in the past']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check availability (simplified - in production, implement proper slot management)
        existing_bookings = Booking.objects.filter(
            property_id=data['property_id'],
            booking_date=booking_date,
            booking_time=data['booking_time'],
            status__in=['PENDING', 'CONFIRMED']
        ).count()
        
        if existing_bookings >= 1:  # Assuming max 1 booking per slot
            return Response({
                'success': False,
                'errors': ['This time slot is not available']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate virtual tour token if needed
        virtual_tour_token = None
        virtual_tour_link = None
        booking_type = data.get('booking_type', 'SITE_VISIT')
        
        if booking_type == 'VIRTUAL_TOUR':
            virtual_tour_token = str(uuid.uuid4())
            virtual_tour_link = f"https://virtualtour.nalindia.com/join/{virtual_tour_token}"
        
        booking = Booking.objects.create(
            user=request.user,
            property_id=data['property_id'],
            booking_type=booking_type,
            booking_date=booking_date,
            booking_time=data['booking_time'],
            duration_minutes=data.get('duration_minutes', 60),
            contact_name=data['contact_name'],
            contact_phone=data['contact_phone'],
            contact_email=data.get('contact_email', request.user.email),
            notes=data.get('notes', ''),
            virtual_tour_link=virtual_tour_link,
            virtual_tour_token=virtual_tour_token
        )
        
        return Response({
            'success': True,
            'data': {
                'booking_id': booking.uuid,
                'status': booking.status,
                'booking_date': booking.booking_date,
                'booking_time': booking.booking_time,
                'virtual_tour_link': booking.virtual_tour_link,
                'message': 'Booking created successfully'
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'errors': ['Failed to create booking']
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_bookings(request):
    """List user's bookings"""
    bookings = Booking.objects.filter(user=request.user).select_related('property').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    booking_data = []
    for booking in bookings:
        booking_data.append({
            'uuid': booking.uuid,
            'property': {
                'uuid': booking.property.uuid,
                'title': booking.property.title,
                'address': booking.property.address
            },
            'booking_type': booking.booking_type,
            'booking_date': booking.booking_date,
            'booking_time': booking.booking_time,
            'duration_minutes': booking.duration_minutes,
            'status': booking.status,
            'contact_name': booking.contact_name,
            'contact_phone': booking.contact_phone,
            'virtual_tour_link': booking.virtual_tour_link,
            'notes': booking.notes,
            'created_at': booking.created_at
        })
    
    return Response({
        'success': True,
        'data': booking_data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booking(request, booking_id):
    """Get booking details"""
    try:
        booking = Booking.objects.select_related('property').get(uuid=booking_id, user=request.user)
        
        return Response({
            'success': True,
            'data': {
                'uuid': booking.uuid,
                'property': {
                    'uuid': booking.property.uuid,
                    'title': booking.property.title,
                    'address': booking.property.address
                },
                'booking_type': booking.booking_type,
                'booking_date': booking.booking_date,
                'booking_time': booking.booking_time,
                'duration_minutes': booking.duration_minutes,
                'status': booking.status,
                'contact_name': booking.contact_name,
                'contact_phone': booking.contact_phone,
                'contact_email': booking.contact_email,
                'virtual_tour_link': booking.virtual_tour_link,
                'notes': booking.notes,
                'created_at': booking.created_at,
                'updated_at': booking.updated_at
            }
        })
        
    except Booking.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Booking not found']
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking_status(request, booking_id):
    """Update booking status"""
    try:
        booking = Booking.objects.get(uuid=booking_id)
        
        # Check permissions
        if booking.user != request.user and booking.property.owner != request.user:
            return Response({
                'success': False,
                'errors': ['Permission denied']
            }, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status not in ['CONFIRMED', 'CANCELLED', 'COMPLETED', 'NO_SHOW']:
            return Response({
                'success': False,
                'errors': ['Invalid status']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = new_status
        
        if new_status == 'CANCELLED':
            booking.cancelled_at = timezone.now()
            booking.cancellation_reason = request.data.get('cancellation_reason', '')
        
        booking.save()
        
        return Response({
            'success': True,
            'data': {
                'booking_id': booking.uuid,
                'status': booking.status,
                'message': f'Booking {new_status.lower()} successfully'
            }
        })
        
    except Booking.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Booking not found']
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_slots(request, property_id):
    """Get available booking slots for a property"""
    try:
        from nal_backend.apps.properties.models import Property
        property_obj = Property.objects.get(uuid=property_id)
        
        # Get date range (next 30 days by default)
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        
        # Generate available slots (simplified - in production, use proper slot management)
        available_slots = []
        current_date = start_date
        
        while current_date <= end_date:
            # Skip weekends for this example
            if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
                # Generate time slots (9 AM to 6 PM)
                for hour in range(9, 18):
                    slot_time = f"{hour:02d}:00"
                    
                    # Check if slot is already booked
                    existing_booking = Booking.objects.filter(
                        property=property_obj,
                        booking_date=current_date,
                        booking_time=slot_time,
                        status__in=['PENDING', 'CONFIRMED']
                    ).exists()
                    
                    if not existing_booking:
                        available_slots.append({
                            'date': current_date.isoformat(),
                            'time': slot_time,
                            'available': True
                        })
            
            current_date += timedelta(days=1)
        
        return Response({
            'success': True,
            'data': {
                'property_id': property_id,
                'available_slots': available_slots[:50]  # Limit to 50 slots
            }
        })
        
    except Property.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Property not found']
        }, status=status.HTTP_404_NOT_FOUND)