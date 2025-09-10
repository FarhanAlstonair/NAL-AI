from rest_framework import serializers
from .models import Property, PropertyMedia, PropertyAmenity

class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = ['id', 'media_url', 'media_type', 'is_primary', 'caption', 'created_at']

class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields = ['id', 'name', 'icon', 'category']

class PropertyListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.profile.full_name', read_only=True)
    
    class Meta:
        model = Property
        fields = ['uuid', 'title', 'price', 'currency', 'property_type', 'status',
                 'city', 'state', 'bedrooms', 'bathrooms', 'area_sqft', 
                 'ribl_score', 'primary_image', 'owner_name', 'created_at']
    
    def get_primary_image(self, obj):
        primary_media = obj.media.filter(is_primary=True, media_type='IMAGE').first()
        return primary_media.media_url if primary_media else None

class PropertyDetailSerializer(serializers.ModelSerializer):
    media = PropertyMediaSerializer(many=True, read_only=True)
    amenities = PropertyAmenitySerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.profile.full_name', read_only=True)
    agent_name = serializers.CharField(source='agent.profile.full_name', read_only=True)
    
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['uuid', 'owner', 'ribl_score', 'urgent_sale_value', 'created_at', 'updated_at']

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'property_type', 'address',
                 'city', 'state', 'pincode', 'latitude', 'longitude', 'bedrooms',
                 'bathrooms', 'area_sqft', 'parking_spaces']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)