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