from rest_framework import viewsets, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User, Group

from .models import Product, Category, Brand, UnitOfMeasurement, Entry, Exit
from .serializers import (
    ProductSerializer, CategorySerializer, BrandSerializer, 
    UnitSerializer, EntrySerializer, ExitSerializer, 
    UserSerializer, GroupSerializer
)


# Serializer para os logs
class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = '__all__'


# ViewSet para leitura dos logs (somente admins)
class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all().order_by('-action_time')
    serializer_class = LogEntrySerializer
    permission_classes = [IsAdminUser]


# View para apagar todos os logs (somente admins)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def clear_logs(request):
    count, _ = LogEntry.objects.all().delete()
    return Response({"detail": f"{count} log(s) apagado(s)."})


# ViewSets com controle de permissão por modelo
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissions]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [DjangoModelPermissions]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasurement.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [DjangoModelPermissions]


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [DjangoModelPermissions]


class ExitViewSet(viewsets.ModelViewSet):
    queryset = Exit.objects.all()
    serializer_class = ExitSerializer
    permission_classes = [DjangoModelPermissions]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissions]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [DjangoModelPermissions]