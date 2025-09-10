from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Property, PropertyMedia
from .serializers import (
    PropertyListSerializer, PropertyDetailSerializer, 
    PropertyCreateSerializer, PropertyMediaSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_properties(request):
    queryset = Property.objects.filter(status='PUBLISHED').select_related('owner__profile')
    
    # Filters
    q = request.GET.get('q')
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(city__icontains=q)
        )
    
    property_type = request.GET.get('property_type')
    if property_type:
        queryset = queryset.filter(property_type=property_type)
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    
    city = request.GET.get('city')
    if city:
        queryset = queryset.filter(city__icontains=city)
    
    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        queryset = queryset.filter(bedrooms__gte=bedrooms)
    
    # Location-based search
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius', 10)  # km
    
    if lat and lng:
        # Simple bounding box search (for production, use PostGIS)
        lat_range = float(radius) / 111.0  # Rough conversion
        lng_range = float(radius) / (111.0 * abs(float(lat)))
        
        queryset = queryset.filter(
            latitude__range=[float(lat) - lat_range, float(lat) + lat_range],
            longitude__range=[float(lng) - lng_range, float(lng) + lng_range]
        )
    
    # Pagination
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    
    paginator = Paginator(queryset, page_size)
    properties = paginator.get_page(page)
    
    serializer = PropertyListSerializer(properties, many=True)
    
    return Response({
        'success': True,
        'data': {
            'properties': serializer.data,
            'pagination': {
                'page': page,
                'pages': paginator.num_pages,
                'count': paginator.count,
                'has_next': properties.has_next(),
                'has_previous': properties.has_previous()
            }
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_property(request, property_id):
    try:
        property_obj = Property.objects.select_related('owner__profile', 'agent__profile').get(uuid=property_id)
        serializer = PropertyDetailSerializer(property_obj)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Property.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Property not found']
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_property(request):
    if request.user.role not in ['SELLER', 'AGENT']:
        return Response({
            'success': False,
            'errors': ['Only sellers and agents can create properties']
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = PropertyCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        property_obj = serializer.save()
        detail_serializer = PropertyDetailSerializer(property_obj)
        return Response({
            'success': True,
            'data': detail_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_property(request, property_id):
    try:
        property_obj = Property.objects.get(uuid=property_id, owner=request.user)
        serializer = PropertyCreateSerializer(property_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            property_obj = serializer.save()
            detail_serializer = PropertyDetailSerializer(property_obj)
            return Response({
                'success': True,
                'data': detail_serializer.data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Property.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Property not found or access denied']
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_property_media(request, property_id):
    try:
        property_obj = Property.objects.get(uuid=property_id, owner=request.user)
        
        media_data = request.data.copy()
        media_data['property'] = property_obj.id
        
        serializer = PropertyMediaSerializer(data=media_data)
        if serializer.is_valid():
            media = serializer.save()
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Property.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Property not found or access denied']
        }, status=status.HTTP_404_NOT_FOUND)