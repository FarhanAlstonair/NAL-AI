from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer, UserProfileSerializer

@api_view(['GET'])
def get_profile(request):
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Profile.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['Profile not found']
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
def update_profile(request):
    try:
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            user_serializer = UserProfileSerializer(request.user)
            return Response({
                'success': True,
                'data': user_serializer.data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'success': False,
            'errors': ['Failed to update profile']
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        from nal_backend.apps.authentication.models import User
        user = User.objects.get(uuid=user_id)
        serializer = UserProfileSerializer(user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'errors': ['User not found']
        }, status=status.HTTP_404_NOT_FOUND)