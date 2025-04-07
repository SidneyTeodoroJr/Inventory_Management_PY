from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User, Group

from .models import Product, Category, Brand, UnitOfMeasurement, Entry, Exit
from .serializers import (
    ProductSerializer, CategorySerializer, BrandSerializer, 
    UnitSerializer, EntrySerializer, ExitSerializer, 
    UserSerializer, GroupSerializer
)
from rest_framework import serializers


# Serializer para os logs
class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = '__all__'


# ViewSet para leitura dos logs
class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all().order_by('-action_time')
    serializer_class = LogEntrySerializer
    permission_classes = [IsAdminUser]  # Apenas admins acessam


# View para apagar todos os logs
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def clear_logs(request):
    count, _ = LogEntry.objects.all().delete()
    return Response({"detail": f"{count} log(s) apagado(s)."})


# Demais ViewSets da API
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasurement.objects.all()
    serializer_class = UnitSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class ExitViewSet(viewsets.ModelViewSet):
    queryset = Exit.objects.all()
    serializer_class = ExitSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer