from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import User, Landlord, Tenant
from .serializers import (
    UserSerializer, LandlordSerializer, TenantSerializer, UserLoginSerializer,
    LandlordListSerializer, TenantListSerializer
)
from listing.serializers import ListingSerializer, ReviewSerializer
from transaction_mgmt.serializers import TransactionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(deleted=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'first_name', 'last_name', 'phone']

    def get_permissions(self):
        if self.action in ['create', 'login', 'register', 'search_users']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user.user_type,
                    'kyc_status': user.kyc_status
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type,
                'kyc_status': user.kyc_status
            }
        })

    @action(detail=True, methods=['post'])
    def verify_kyc(self, request, pk=None):
        user = self.get_object()
        user.kyc_status = 'verified'
        user.save()
        return Response({'status': 'KYC verified'})

    @action(detail=True, methods=['post'])
    def reject_kyc(self, request, pk=None):
        user = self.get_object()
        user.kyc_status = 'rejected'
        user.save()
        return Response({'status': 'KYC rejected'})

    @action(detail=False, methods=['get'])
    def search_users(self, request):
        """
        Tìm kiếm người dùng (cả chủ nhà và người thuê) theo từ khóa
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Vui lòng cung cấp từ khóa tìm kiếm (q)"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Tìm kiếm người dùng theo họ tên, email, số điện thoại
        users = User.objects.filter(deleted=False).filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(phone__icontains=query)
        )
        
        # Phân loại kết quả theo loại người dùng
        landlords = []
        tenants = []
        
        for user in users:
            # Kiểm tra user_type không phân biệt chữ hoa/chữ thường
            user_type_lower = user.user_type.lower()
            
            if user_type_lower == 'landlord':
                try:
                    # Truy vấn trực tiếp để tránh lỗi
                    landlord = Landlord.objects.get(user_id=user.id)
                    landlord_data = LandlordListSerializer(landlord).data
                    landlords.append(landlord_data)
                except Landlord.DoesNotExist:
                    # Thêm dữ liệu cơ bản nếu không có mô hình Landlord
                    landlords.append({
                        "id": user.id,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "user_type": user.user_type
                        }
                    })
            elif user_type_lower == 'tenant':
                try:
                    # Truy vấn trực tiếp để tránh lỗi
                    tenant = Tenant.objects.get(user_id=user.id)
                    tenant_data = TenantListSerializer(tenant).data
                    tenants.append(tenant_data)
                except Tenant.DoesNotExist:
                    # Thêm dữ liệu cơ bản nếu không có mô hình Tenant
                    tenants.append({
                        "id": user.id,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "user_type": user.user_type
                        }
                    })
        
        return Response({
            "landlords": landlords,
            "tenants": tenants,
            "total_results": len(landlords) + len(tenants)
        })

class LandlordViewSet(viewsets.ModelViewSet):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'user__phone']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LandlordListSerializer
        return LandlordSerializer

    @action(detail=True, methods=['get'])
    def listings(self, request, pk=None):
        landlord = self.get_object()
        listings = landlord.listings.filter(deleted=False)
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        landlord = self.get_object()
        transactions = landlord.user.received_transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'user__phone']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TenantListSerializer
        return TenantSerializer

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        tenant = self.get_object()
        transactions = tenant.user.sent_transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        tenant = self.get_object()
        reviews = tenant.user.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data) 