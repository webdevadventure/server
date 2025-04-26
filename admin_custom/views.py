from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Admin, ListingApproval, Alert, AlertType, ApprovalAction
from user_mgmt.models import User, Landlord, Tenant
from listing.models import Listing, ListingStatus
from .serializers import (
    AdminSerializer, ListingApprovalSerializer, AlertSerializer, 
    AlertTypeSerializer, AdminStatisticsSerializer, LandlordApprovalSerializer,
    AdminUserSerializer
)
from listing.serializers import ListingSerializer
from user_mgmt.serializers import UserSerializer

class IsAdminUser(permissions.BasePermission):
    """
    Quyền hạn dành cho admin user
    """
    def has_permission(self, request, view):
        # Kiểm tra user là admin
        if not request.user or not request.user.is_authenticated:
            return False
        
        try:
            admin = Admin.objects.get(user=request.user)
            return True
        except Admin.DoesNotExist:
            return False

class AdminViewSet(viewsets.ModelViewSet):
    """
    Quản lý admin và cung cấp tính năng dashboard
    """
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Trả về thống kê tổng quan cho dashboard
        """
        try:
            # Tính toán thống kê trực tiếp tại đây thay vì phụ thuộc hoàn toàn vào serializer
            now = timezone.now()
            first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            total_users = User.objects.filter(deleted=False).count()
            total_landlords = Landlord.objects.count()
            total_tenants = Tenant.objects.count()
            total_listings = Listing.objects.filter(deleted=False).count()
            pending_listings = Listing.objects.filter(deleted=False, status='pending').count()
            approved_listings = Listing.objects.filter(deleted=False, status='approved').count()
            rejected_listings = Listing.objects.filter(deleted=False, status='rejected').count()
            new_users_this_month = User.objects.filter(date_joined__gte=first_day_of_month, deleted=False).count()
            new_listings_this_month = Listing.objects.filter(posting_date__gte=first_day_of_month, deleted=False).count()
            avg_price_result = Listing.objects.filter(deleted=False, status='approved').aggregate(Avg('price'))
            average_listing_price = avg_price_result['price__avg'] if avg_price_result['price__avg'] is not None else 0
            
            # Trả về dữ liệu thống kê trực tiếp
            return Response({
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
            })
        except Exception as e:
            # Ghi log lỗi (nếu cần)
            print(f"Error in statistics: {str(e)}")
            
            # Trả về giá trị mặc định để tránh null
            return Response({
                'total_users': 0,
                'total_landlords': 0,
                'total_tenants': 0,
                'total_listings': 0,
                'pending_listings': 0,
                'approved_listings': 0,
                'rejected_listings': 0,
                'new_users_this_month': 0,
                'new_listings_this_month': 0,
                'average_listing_price': 0,
            })
    
    @action(detail=False, methods=['get'])
    def pending_listings(self, request):
        """
        Danh sách bất động sản đang chờ phê duyệt
        """
        listings = Listing.objects.filter(
            deleted=False, 
            status=ListingStatus.PENDING
        ).order_by('-posting_date')
        
        page = self.paginate_queryset(listings)
        if page is not None:
            serializer = ListingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_landlords(self, request):
        """
        Danh sách landlord đang chờ phê duyệt KYC
        """
        landlords = User.objects.filter(
            deleted=False,
            user_type__iexact='landlord',
            kyc_status='pending'
        ).order_by('-date_joined')
        
        page = self.paginate_queryset(landlords)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = UserSerializer(landlords, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def approve_listing(self, request):
        """
        Phê duyệt hoặc từ chối bất động sản
        """
        listing_id = request.data.get('listing_id')
        action = request.data.get('action')
        reason = request.data.get('reason', '')
        
        if not listing_id or action not in [ApprovalAction.APPROVE, ApprovalAction.REJECT]:
            return Response(
                {"error": "Cần cung cấp listing_id và action hợp lệ (approve/reject)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            listing = Listing.objects.get(id=listing_id, deleted=False)
        except Listing.DoesNotExist:
            return Response(
                {"error": "Không tìm thấy bất động sản"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Cập nhật trạng thái listing
        if action == ApprovalAction.APPROVE:
            listing.status = ListingStatus.APPROVED
        else:
            listing.status = ListingStatus.REJECTED
        
        listing.save()
        
        # Lưu lịch sử phê duyệt
        approval = ListingApproval.objects.create(
            listing=listing,
            admin=request.user,
            action=action,
            reason=reason
        )
        
        serializer = ListingApprovalSerializer(approval)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def approve_landlord(self, request):
        """
        Phê duyệt hoặc từ chối KYC của landlord
        """
        serializer = LandlordApprovalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        user_id = data.get('user_id')
        approve = data.get('approve')
        reason = data.get('reason', '')
        
        try:
            user = User.objects.get(id=user_id, user_type__iexact='landlord', deleted=False)
        except User.DoesNotExist:
            return Response(
                {"error": "Không tìm thấy landlord"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Cập nhật trạng thái KYC
        if approve:
            user.kyc_status = 'verified'
        else:
            user.kyc_status = 'rejected'
        
        user.save()
        
        return Response({
            "id": user.id,
            "email": user.email,
            "kyc_status": user.kyc_status,
            "message": "Đã cập nhật trạng thái KYC thành công"
        })
    
    @action(detail=False, methods=['get'])
    def user_management(self, request):
        """
        Quản lý người dùng (tìm kiếm, lọc)
        """
        query = request.query_params.get('q', '')
        user_type = request.query_params.get('user_type', '').lower()
        
        users = User.objects.filter(deleted=False)
        
        # Tìm kiếm
        if query:
            users = users.filter(
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(phone__icontains=query)
            )
        
        # Lọc theo loại người dùng
        if user_type in ['tenant', 'landlord']:
            users = users.filter(user_type__iexact=user_type)
        
        # Sắp xếp
        users = users.order_by('-date_joined')
        
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = AdminUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def disable_user(self, request):
        """
        Vô hiệu hóa tài khoản người dùng
        """
        user_id = request.data.get('user_id')
        reason = request.data.get('reason', '')
        
        if not user_id:
            return Response(
                {"error": "Cần cung cấp user_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Không tìm thấy người dùng"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Đánh dấu đã xóa thay vì xóa hoàn toàn
        user.deleted = True
        user.save()
        
        return Response({
            "message": f"Đã vô hiệu hóa người dùng {user.email}",
            "reason": reason
        })
    
    @action(detail=False, methods=['get'])
    def listing_management(self, request):
        """
        Quản lý bất động sản (tìm kiếm, lọc)
        """
        query = request.query_params.get('q', '')
        status_filter = request.query_params.get('status', '')
        property_type = request.query_params.get('property_type', '')
        
        listings = Listing.objects.filter(deleted=False)
        
        # Tìm kiếm
        if query:
            listings = listings.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(specific_address__icontains=query)
            )
        
        # Lọc theo trạng thái
        if status_filter and status_filter in ['pending', 'approved', 'rejected']:
            listings = listings.filter(status=status_filter)
        
        # Lọc theo loại bất động sản
        if property_type and property_type in ['room', 'apartment', 'house']:
            listings = listings.filter(property_type=property_type)
        
        # Sắp xếp
        listings = listings.order_by('-posting_date')
        
        page = self.paginate_queryset(listings)
        if page is not None:
            serializer = ListingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

class AlertViewSet(viewsets.ModelViewSet):
    """
    Quản lý các cảnh báo
    """
    queryset = Alert.objects.all().order_by('-detection_time')
    serializer_class = AlertSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['alert_type', 'listing']
    search_fields = ['description']

class AlertTypeViewSet(viewsets.ModelViewSet):
    """
    Quản lý các loại cảnh báo
    """
    queryset = AlertType.objects.all()
    serializer_class = AlertTypeSerializer
    permission_classes = [IsAdminUser] 