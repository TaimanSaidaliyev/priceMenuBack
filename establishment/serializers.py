from rest_framework import serializers, generics
from .models import *
from django.core.files import File


class EstablishmentAllListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ('__all__')
        depth = 2


class ListOfProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('__all__')
        depth = 2


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'title', 'description', 'price', 'old_price', 'photo', 'is_active', 'is_published']


class MenuCategorySerializer(serializers.ModelSerializer):
    products = ProductsSerializer(source='get_products_menu_category', many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = ['id', 'category_title', 'products']


class MenuSerializer(serializers.ModelSerializer):
    categories = MenuCategorySerializer(source='get_menu_category_menu', many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'menu_title', 'photo', 'categories', 'establishment']
        depth = 10


class MenuListSerializer(serializers.ModelSerializer):
    categories = MenuCategorySerializer(source='get_menu_category_menu', many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('__all__')


class CategoryListByMenuId(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ('__all__')


class ProductListByCategoryId(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('__all__')


class PromotionsByEstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        fields = ('__all__')
        depth = 0


class MenuAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('__all__')


class CategoryAddSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(source='get_products_menu_category', many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = ('__all__')


class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('__all__')