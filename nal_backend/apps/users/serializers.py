from rest_framework import serializers
from .models import Profile
from nal_backend.apps.authentication.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'photo_url', 'kyc_status', 'address', 'city', 
                 'state', 'country', 'pincode', 'date_of_birth', 'updated_at']
        read_only_fields = ['kyc_status', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['uuid', 'email', 'username', 'phone', 'role', 'is_verified', 
                 'created_at', 'profile']
        read_only_fields = ['uuid', 'role', 'is_verified', 'created_at']