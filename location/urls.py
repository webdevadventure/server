from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProvinceViewSet, CityViewSet, DistrictViewSet,
    WardViewSet, StreetViewSet
)

router = DefaultRouter()
router.register(r'provinces', ProvinceViewSet)
router.register(r'cities', CityViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'wards', WardViewSet)
router.register(r'streets', StreetViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 