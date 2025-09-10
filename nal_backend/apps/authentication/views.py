from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .models import User, DeviceSession
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        device_id = serializer.validated_data.get('device_id')
        device_type = serializer.validated_data.get('device_type', 'web')
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Track device session
        if device_id:
            DeviceSession.objects.update_or_create(
                user=user,
                device_id=device_id,
                defaults={
                    'device_type': device_type,
                    'refresh_token_hash': make_password(str(refresh)),
                    'is_active': True
                }
            )
        
        return Response({
            'success': True,
            'data': {
                'access': str(access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'success': True,
            'data': {
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'success': False,
                'errors': ['Refresh token required']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token
        
        return Response({
            'success': True,
            'data': {
                'access': str(access_token),
                'refresh': str(refresh)
            }
        })
    except Exception as e:
        return Response({
            'success': False,
            'errors': ['Invalid refresh token']
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        device_id = request.data.get('device_id')
        
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        if device_id:
            DeviceSession.objects.filter(
                user=request.user,
                device_id=device_id
            ).update(is_active=False)
        
        return Response({
            'success': True,
            'data': {'message': 'Logged out successfully'}
        })
    except Exception:
        return Response({
            'success': True,
            'data': {'message': 'Logged out successfully'}
        })