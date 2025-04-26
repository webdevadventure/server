from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminViewSet, AlertViewSet, AlertTypeViewSet

router = DefaultRouter()
router.register(r'admin', AdminViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'alert-types', AlertTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 