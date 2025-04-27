from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, ReviewViewSet, ListingImageViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'images', ListingImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 