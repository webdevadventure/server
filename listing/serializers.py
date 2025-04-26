from rest_framework import serializers
from .models import Listing, ListingImage, Review
from location.serializers import ProvinceSerializer, DistrictSerializer, WardSerializer, StreetSerializer
from user_mgmt.serializers import UserSerializer

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image_url']
        read_only_fields = ['id']

class ReviewSerializer(serializers.ModelSerializer):
    tenant_details = UserSerializer(source='tenant', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'tenant', 'tenant_details', 'listing', 'review_text', 'rating', 'review_date']
        read_only_fields = ['id', 'review_date']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.URLField(),
        write_only=True,
        required=False
    )
    landlord_details = UserSerializer(source='landlord', read_only=True)
    province_details = ProvinceSerializer(source='province', read_only=True)
    district_details = DistrictSerializer(source='district', read_only=True)
    ward_details = WardSerializer(source='ward', read_only=True)
    street_details = StreetSerializer(source='street', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'landlord', 'landlord_details', 'title', 'description', 
            'price', 'property_type', 'province', 'province_details', 
            'district', 'district_details', 'ward', 'ward_details',
            'street', 'street_details', 'specific_address', 'status',
            'posting_date', 'deleted', 'images', 'uploaded_images',
            'reviews', 'average_rating'
        ]
        read_only_fields = ['id', 'status', 'posting_date', 'deleted', 'average_rating']
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        listing = Listing.objects.create(**validated_data)
        
        for image_url in uploaded_images:
            ListingImage.objects.create(listing=listing, image_url=image_url)
        
        return listing
    
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        instance = super().update(instance, validated_data)
        
        if uploaded_images:
            for image_url in uploaded_images:
                ListingImage.objects.create(listing=instance, image_url=image_url)
        
        return instance 