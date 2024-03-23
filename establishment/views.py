from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import *
from .serializers import *
from rest_framework import status


class EstablishmentAllListView(APIView):
    def get(self, request, establishment_id):
        establishment = Establishment.objects.get(pk=establishment_id)
        return Response(
            {
            'establishment': EstablishmentAllListSerializer(establishment, many=False).data
            }
        )


class ListOfProducts(APIView):
    def get(self, request, establishment_id):
        list = Menu.objects.filter(establishment=establishment_id)
        return Response(
            {
            'list': MenuSerializer(list, many=True).data
            }
        )


class GetPromotionsByEstablishment(APIView):
    def get(self, request, establishment_id):
        list = Promotions.objects.filter(establishment=establishment_id)
        return Response(
            {
                'promotions': PromotionsByEstablishmentSerializer(list, many=True).data
            }
        )


class GetMenuListByEstablishment(APIView):
    def get(self, request, establishment_id):
        list = Menu.objects.filter(establishment=establishment_id)
        return Response(
            {
                'menus': MenuListSerializer(list, many=True).data
            }
        )


class GetCategoryListByMenuId(APIView):
    def get(self, request, menu_id):
        list = MenuCategory.objects.filter(menu=menu_id)
        return Response(
            {
                'categories': CategoryListByMenuId(list, many=True).data
            }
        )


class GetProductListByCategoryId(APIView):
    def get(self, request, category_id):
        list = Products.objects.filter(category_id=category_id)
        return Response(
            {
                'products': ProductListByCategoryId(list, many=True).data
            }
        )


class GetProductById(APIView):
    def get(self, request, product_id):
        list = Products.objects.get(id=product_id)
        return Response(
            {
                'product': ProductListByCategoryId(list, many=False).data
            }
        )


class AddMenuByEstablishment(APIView):
    def post(self, request):
        serializer = MenuAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            menu_instance = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return Response({"error": "Menu does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuAddSerializer(menu_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        list = Menu.objects.get(pk=pk)
        return Response(
            {
                'menu': MenuListSerializer(list, many=False).data
            }
        )

    def delete(self, request, pk):
        try:
            menu_instance = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return Response({"error": "Menu does not exist"}, status=status.HTTP_404_NOT_FOUND)

        menu_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddCategoryByMenu(APIView):
    def post(self, request):
        serializer = CategoryAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            category_instance = MenuCategory.objects.get(pk=pk)
        except MenuCategory.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryAddSerializer(category_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        list = MenuCategory.objects.get(pk=pk)
        return Response(
            {
                'category': CategoryAddSerializer(list, many=False).data
            }
        )

    def delete(self, request, pk):
        try:
            category_instance = MenuCategory.objects.get(pk=pk)
        except MenuCategory.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)

        category_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddProductByCategory(APIView):
    def post(self, request):
        serializer = ProductAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            product_instance = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductAddSerializer(product_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        list = Products.objects.get(pk=pk)
        return Response(
            {
                'product': ProductAddSerializer(list, many=False).data
            }
        )

    def delete(self, request, pk):
        try:
            product_instance = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        product_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateProductSorting(APIView):
    def put(self, request):
        data = request.data
        for item in data:
            product_id = item.get('id')
            sorting_number = item.get('sorting_number')
            print(product_id, sorting_number)
            try:
                product = Products.objects.get(pk=product_id)
                product.sorting_number = sorting_number
                product.save()
            except Products.DoesNotExist:
                pass

        return Response({'message': 'Products sorting updated successfully'}, status=status.HTTP_200_OK)


class UpdateCategorySorting(APIView):
    def put(self, request):
        data = request.data
        for item in data:
            product_id = item.get('id')
            sorting_number = item.get('sorting_number')
            print(product_id, sorting_number)
            try:
                category = MenuCategory.objects.get(pk=product_id)
                category.sorting_number = sorting_number
                category.save()
            except MenuCategory.DoesNotExist:
                pass

        return Response({'message': 'Category sorting updated successfully'}, status=status.HTTP_200_OK)
