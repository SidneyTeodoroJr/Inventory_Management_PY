from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, BrandViewSet, UnitViewSet, 
    EntryViewSet, ExitViewSet, UserViewSet, GroupViewSet, 
    LogEntryViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'units', UnitViewSet)
router.register(r'entries', EntryViewSet)
router.register(r'exits', ExitViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'logs', LogEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
