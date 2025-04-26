from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Listing, ListingImage, Review, PropertyType, ListingStatus
from .serializers import ListingSerializer, ListingImageSerializer, ReviewSerializer
from user_mgmt.models import User

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