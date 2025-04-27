from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Listing, ListingImage, Review, PropertyType, ListingStatus
from .serializers import ListingSerializer, ListingImageSerializer, ReviewSerializer
from user_mgmt.models import User
from location.models import Province, District, Ward, Street

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Listing owner can modify
        if hasattr(obj, 'landlord'):
            return obj.landlord == request.user
        
        # Review author can modify
        if hasattr(obj, 'tenant'):
            return obj.tenant == request.user
        
        return False

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.filter(deleted=False)
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'status', 'province', 'district', 'ward']
    search_fields = ['title', 'description', 'specific_address']
    ordering_fields = ['price', 'area', 'posting_date']
    ordering = ['-posting_date']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by area range
        min_area = self.request.query_params.get('min_area')
        max_area = self.request.query_params.get('max_area')
        
        if min_area:
            queryset = queryset.filter(area__gte=min_area)
        if max_area:
            queryset = queryset.filter(area__lte=max_area)
        
        # Filter by landlord
        landlord_id = self.request.query_params.get('landlord')
        if landlord_id:
            queryset = queryset.filter(landlord_id=landlord_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)
    
    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        listing = self.get_object()
        
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        listing.status = ListingStatus.APPROVED
        listing.save()
        return Response({"status": "Listing approved"})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        listing = self.get_object()
        
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        listing.status = ListingStatus.REJECTED
        listing.save()
        return Response({"status": "Listing rejected"})
    
    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        listing = self.get_object()
        
        similar_listings = Listing.objects.filter(
            ~Q(id=listing.id),
            deleted=False,
            status=ListingStatus.APPROVED,
            property_type=listing.property_type
        )
        
        # Try to match by location
        if listing.ward:
            ward_listings = similar_listings.filter(ward=listing.ward)
            if ward_listings.count() >= 3:
                similar_listings = ward_listings
        
        if similar_listings.count() < 3 and listing.district:
            district_listings = similar_listings.filter(district=listing.district)
            if district_listings.count() >= 3:
                similar_listings = district_listings
        
        if similar_listings.count() < 3 and listing.province:
            province_listings = similar_listings.filter(province=listing.province)
            if province_listings.count() >= 3:
                similar_listings = province_listings
        
        # Limit to 6 similar listings
        similar_listings = similar_listings[:6]
        
        serializer = self.get_serializer(similar_listings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Tìm kiếm nâng cao cho phòng/căn hộ dựa trên từ khóa
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Vui lòng cung cấp từ khóa tìm kiếm (q)"}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        # Lấy tất cả listings có status đã được phê duyệt
        listings = Listing.objects.filter(deleted=False, status=ListingStatus.APPROVED)
        
        # Tìm kiếm trực tiếp trong listings
        direct_matches = listings.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(specific_address__icontains=query)
        )
        
        # Tìm kiếm trong thông tin location
        province_matches = Province.objects.filter(name__icontains=query)
        district_matches = District.objects.filter(name__icontains=query)
        ward_matches = Ward.objects.filter(name__icontains=query)
        street_matches = Street.objects.filter(name__icontains=query)
        
        # Tìm kiếm listings từ kết quả location
        location_matches = Listing.objects.none()
        
        if province_matches.exists():
            province_listings = listings.filter(province__in=province_matches)
            location_matches = location_matches.union(province_listings)
            
        if district_matches.exists():
            district_listings = listings.filter(district__in=district_matches)
            location_matches = location_matches.union(district_listings)
            
        if ward_matches.exists():
            ward_listings = listings.filter(ward__in=ward_matches)
            location_matches = location_matches.union(ward_listings)
            
        if street_matches.exists():
            street_listings = listings.filter(street__in=street_matches)
            location_matches = location_matches.union(street_listings)
        
        # Kết hợp tất cả kết quả và loại bỏ trùng lặp
        all_results = direct_matches.union(location_matches)
        
        # Thêm bộ lọc thông thường nếu có
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        min_area = request.query_params.get('min_area')
        max_area = request.query_params.get('max_area')
        property_type = request.query_params.get('property_type')
        
        if min_price:
            all_results = all_results.filter(price__gte=min_price)
        if max_price:
            all_results = all_results.filter(price__lte=max_price)
        if min_area:
            all_results = all_results.filter(area__gte=min_area)
        if max_area:
            all_results = all_results.filter(area__lte=max_area)
        if property_type:
            all_results = all_results.filter(property_type=property_type)
        
        # Sắp xếp kết quả
        ordering = request.query_params.get('ordering', '-posting_date')
        if ordering:
            all_results = all_results.order_by(ordering)
        
        # Phân trang kết quả
        page = self.paginate_queryset(all_results)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(all_results, many=True)
        return Response({
            "results": serializer.data,
            "count": all_results.count()
        })

class ListingImageViewSet(viewsets.ModelViewSet):
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        listing_id = self.request.query_params.get('listing')
        
        if listing_id:
            queryset = queryset.filter(listing_id=listing_id)
        
        return queryset
    
    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing')
        listing = Listing.objects.get(id=listing_id)
        
        if listing.landlord != self.request.user:
            self.permission_denied(
                self.request,
                message="You do not have permission to add images to this listing."
            )
        
        serializer.save()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['listing', 'tenant']
    ordering_fields = ['review_date', 'rating']
    ordering = ['-review_date']
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        min_rating = self.request.query_params.get('min_rating')
        
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        
        return queryset 