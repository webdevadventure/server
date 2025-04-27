from rest_framework import serializers
from .models import Admin, ListingApproval, Alert, AlertType
from user_mgmt.models import User, Landlord, Tenant
from listing.models import Listing
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'kyc_status', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']

class AdminSerializer(serializers.ModelSerializer):
    user = AdminUserSerializer()
    
    class Meta:
        model = Admin
        fields = ['user', 'assigned_date']

class ListingApprovalSerializer(serializers.ModelSerializer):
    admin_email = serializers.SerializerMethodField()
    
    class Meta:
        model = ListingApproval
        fields = ['id', 'listing', 'admin', 'admin_email', 'action', 'reason', 'approval_date']
        read_only_fields = ['id', 'admin', 'admin_email', 'approval_date']

    def get_admin_email(self, obj):
        return obj.admin.email

class AlertTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertType
        fields = ['id', 'name']

class AlertSerializer(serializers.ModelSerializer):
    alert_type_name = serializers.SerializerMethodField()
    listing_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = ['id', 'listing', 'listing_title', 'alert_type', 'alert_type_name', 'description', 'detection_time']
        read_only_fields = ['id', 'detection_time']
    
    def get_alert_type_name(self, obj):
        return obj.alert_type.name
    
    def get_listing_title(self, obj):
        return obj.listing.title

class AdminStatisticsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_landlords = serializers.IntegerField()
    total_tenants = serializers.IntegerField()
    total_listings = serializers.IntegerField()
    pending_listings = serializers.IntegerField()
    approved_listings = serializers.IntegerField()
    rejected_listings = serializers.IntegerField()
    new_users_this_month = serializers.IntegerField()
    new_listings_this_month = serializers.IntegerField()
    average_listing_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    def to_representation(self, instance):
        # No instance is needed, we'll calculate statistics here
        now = timezone.now()
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Đảm bảo trả về giá trị không null
        try:
            total_users = User.objects.filter(deleted=False).count()
        except:
            total_users = 0
            
        try:
            total_landlords = Landlord.objects.count()
        except:
            total_landlords = 0
            
        try:
            total_tenants = Tenant.objects.count()
        except:
            total_tenants = 0
            
        try:
            total_listings = Listing.objects.filter(deleted=False).count()
        except:
            total_listings = 0
            
        try:
            pending_listings = Listing.objects.filter(deleted=False, status='pending').count()
        except:
            pending_listings = 0
            
        try:
            approved_listings = Listing.objects.filter(deleted=False, status='approved').count()
        except:
            approved_listings = 0
            
        try:
            rejected_listings = Listing.objects.filter(deleted=False, status='rejected').count()
        except:
            rejected_listings = 0
            
        try:
            new_users_this_month = User.objects.filter(date_joined__gte=first_day_of_month, deleted=False).count()
        except:
            new_users_this_month = 0
            
        try:
            new_listings_this_month = Listing.objects.filter(posting_date__gte=first_day_of_month, deleted=False).count()
        except:
            new_listings_this_month = 0
            
        try:
            avg_price = Listing.objects.filter(deleted=False, status='approved').aggregate(Avg('price'))['price__avg']
            average_listing_price = avg_price if avg_price is not None else 0
        except:
            average_listing_price = 0
        
        statistics = {
            'total_users': total_users,
            'total_landlords': total_landlords,
            'total_tenants': total_tenants,
            'total_listings': total_listings,
            'pending_listings': pending_listings,
            'approved_listings': approved_listings,
            'rejected_listings': rejected_listings,
            'new_users_this_month': new_users_this_month,
            'new_listings_this_month': new_listings_this_month,
            'average_listing_price': average_listing_price,
        }
        
        return statistics

class LandlordApprovalSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    approve = serializers.BooleanField()
    reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id, user_type__iexact='landlord')
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found or not a landlord")
        
        return data 

class ListingApprovalDetailSerializer(serializers.ModelSerializer):
    landlord = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    pricing = serializers.SerializerMethodField()
    rules = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'property_type', 'room_type',
            'landlord', 'amenities', 'images', 'location', 'pricing',
            'rules', 'status', 'created_at', 'updated_at'
        ]

    def get_landlord(self, obj):
        return {
            'id': obj.landlord.id,
            'name': obj.landlord.user.get_full_name(),
            'email': obj.landlord.user.email,
            'phone': obj.landlord.user.phone,
            'kyc_status': obj.landlord.kyc_status
        }

    def get_amenities(self, obj):
        return {
            'bedrooms': obj.bedrooms,
            'bathrooms': obj.bathrooms,
            'area': obj.area,
            'furnished': obj.furnished,
            'air_conditioning': obj.air_conditioning,
            'wifi': obj.wifi,
            'parking': obj.parking,
            'pets_allowed': obj.pets_allowed,
            'smoking_allowed': obj.smoking_allowed
        }

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    def get_location(self, obj):
        return {
            'address': obj.address,
            'city': obj.city,
            'state': obj.state,
            'country': obj.country,
            'zip_code': obj.zip_code,
            'latitude': obj.latitude,
            'longitude': obj.longitude
        }

    def get_pricing(self, obj):
        return {
            'price': obj.price,
            'deposit': obj.deposit,
            'utilities_included': obj.utilities_included,
            'additional_fees': obj.additional_fees
        }

    def get_rules(self, obj):
        return {
            'check_in_time': obj.check_in_time,
            'check_out_time': obj.check_out_time,
            'minimum_stay': obj.minimum_stay,
            'maximum_stay': obj.maximum_stay,
            'house_rules': obj.house_rules
        }

    def get_status(self, obj):
        return {
            'current_status': obj.status,
            'is_available': obj.is_available,
            'is_featured': obj.is_featured,
            'is_verified': obj.is_verified
        } 