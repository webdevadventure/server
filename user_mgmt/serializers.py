from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Landlord, Tenant

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 
                 'phone', 'user_type', 'kyc_status')
        read_only_fields = ('id', 'kyc_status', 'email', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True}
        }

    def validate(self, data):
        if self.instance is None:  # Only for create
            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError("Passwords do not match")
        elif data.get('password') and data.get('confirm_password'):  # For update if password provided
            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
    def update(self, instance, validated_data):
        # Remove confirm_password if it exists
        validated_data.pop('confirm_password', None)
        
        # Handle password update if provided
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance

class UserBasicInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone', 'user_type', 'kyc_status')
        read_only_fields = ('id', 'email', 'full_name', 'user_type', 'kyc_status')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class LandlordSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Landlord
        fields = ('user', 'bank_info', 'average_rating', 'number_of_reviews')
        read_only_fields = ('average_rating', 'number_of_reviews')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'landlord'
        user = UserSerializer().create(user_data)
        landlord = Landlord.objects.create(user=user, **validated_data)
        return landlord

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            UserSerializer().update(instance.user, user_data)
        return super().update(instance, validated_data)

class LandlordListSerializer(serializers.ModelSerializer):
    user = UserBasicInfoSerializer(read_only=True)
    
    class Meta:
        model = Landlord
        fields = ('user', 'average_rating', 'number_of_reviews')
        read_only_fields = ('average_rating', 'number_of_reviews')

class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Tenant
        fields = ('user', 'rental_history')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'tenant'
        user = UserSerializer().create(user_data)
        tenant = Tenant.objects.create(user=user, **validated_data)
        return tenant

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            UserSerializer().update(instance.user, user_data)
        return super().update(instance, validated_data)

class TenantListSerializer(serializers.ModelSerializer):
    user = UserBasicInfoSerializer(read_only=True)
    
    class Meta:
        model = Tenant
        fields = ('user', 'rental_history')

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField() 