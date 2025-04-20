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


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id', 'title', 'color', 'icon']


class ProductsSerializer(serializers.ModelSerializer):
    tags = ProductTagSerializer(many=True, read_only=True)
    child_products = serializers.SerializerMethodField()

    def get_child_products(self, obj):
        children = Products.objects.filter(parent=obj)
        return ChildProductSerializer(children, many=True, context=self.context).data

    class Meta:
        model = Products
        fields = ['id', 'title', 'description', 'price', 'old_price', 'photo', 'is_active', 'is_published', 'sorting_number', 'is_recommended', 'tags', 'child_products', 'category']


class MenuCategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        fields = ['id', 'category_title', 'products', 'sorting_number']

    def get_products(self, obj):
        qs = obj.get_products_menu_category.all()
        # qs = obj.get_products_menu_category.filter(parent__isnull=True)
        return ProductsSerializer(qs, many=True, read_only=True).data


class MenuSerializer(serializers.ModelSerializer):
    categories = MenuCategorySerializer(source='get_menu_category_menu', many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'menu_title', 'photo', 'categories', 'establishment', 'sorting_number']
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
    tags = ProductTagSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ('__all__')
        # fields = ['id', 'title', 'description', 'price', 'old_price', 'photo', 'is_active', 'is_published', 'sorting_number', 'is_recommended', 'tags', 'category', 'establishment', 'is_recommended']


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


class ChildProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'title', 'price')


class ProductAddSerializer(serializers.ModelSerializer):
    tags = ProductTagSerializer(many=True, required=False)
    child_products = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ('__all__')

    def get_child_products(self, obj):
        children = Products.objects.filter(parent=obj)
        return ChildProductSerializer(children, many=True, context=self.context).data


class ProductPutSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=ProductTag.objects.all(),  # Используйте модель тегов
        many=True
    )

    class Meta:
        model = Products
        fields = '__all__'


class ProductWithCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = Products
        fields = ['id', 'title', 'description', 'price', 'count', 'is_active', 'additional_code']


class EstablishmentChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ['id', 'title', 'description', 'default_color', 'photo', 'backgroundImage', 'menu_view_type', 'workTime', 'tags_type_view']


class EstablishmentReviewSerializer(serializers.ModelSerializer):
    ip_address = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = EstablishmentReviews
        fields = [
            'id',
            'ip_address',
            'description',
            'coordinate_w',
            'coordinate_h',
            'photo',
            'created_at',
            'updated_at',
            'establishment',
        ]
