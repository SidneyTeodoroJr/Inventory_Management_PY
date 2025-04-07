from rest_framework import serializers
from .models import Product, Category, Brand, UnitOfMeasurement, Entry, Exit
from django.contrib.auth.models import User, Group

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

class ExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exit
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']