from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import *
from .serializers import *
from rest_framework import status, permissions
from django.contrib.auth.models import User
from userProfile.models import Profile


def get_establishment_of_user(user_id):
    user = Profile.objects.get(user_id=user_id)
    return user.company.pk


def is_access(request):
    if int(str(get_establishment_of_user(request.user.pk))) == int(str(request.data['establishment'])):
        return True
    else:
        return False


def is_access_establishment(request):
    if int(str(get_establishment_of_user(request.user.pk))) == int(str(request.data['id'])):
        return True
    else:
        return False


def is_access_menu_pk(request, pk):
    menu = Menu.objects.get(pk=pk)
    if get_establishment_of_user(request.user.pk) == menu.establishment.pk:
        return True
    else:
        return False


def is_access_category_pk(request, pk):
    menu_category = MenuCategory.objects.get(pk=pk)
    if get_establishment_of_user(request.user.pk) == menu_category.establishment.pk:
        return True
    else:
        return False


def is_access_product_pk(request, pk):
    product = Products.objects.get(pk=pk)
    if get_establishment_of_user(request.user.pk) == product.establishment.pk:
        return True
    else:
        return False


class EstablishmentAllListView(APIView):
    def get(self, request, establishment_id):
        establishment = Establishment.objects.get(pk=establishment_id)
        return Response(
            {
            'establishment': EstablishmentAllListSerializer(establishment, many=False).data
            }
        )

    def put(self, request, establishment_id):
        if is_access_establishment(request):
            try:
                establishment_instance = Establishment.objects.get(pk=establishment_id)
            except Establishment.DoesNotExist:
                return Response({"error": "Establishment does not exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = EstablishmentChangeSerializer(establishment_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
        if is_access(request):
            serializer = MenuAddSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'У вас недостаточно прав'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if is_access(request):
            try:
                menu_instance = Menu.objects.get(pk=pk)
            except Menu.DoesNotExist:
                return Response({"error": "Menu does not exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = MenuAddSerializer(menu_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        if is_access_menu_pk(request, pk):
            list = Menu.objects.get(pk=pk, establishment=get_establishment_of_user(request.user.pk))
            return Response(
                {
                    'menu': MenuListSerializer(list, many=False).data
                }
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if is_access_menu_pk(request, pk):
            try:
                menu_instance = Menu.objects.get(pk=pk)
            except Menu.DoesNotExist:
                return Response({"error": "Menu does not exist"}, status=status.HTTP_404_NOT_FOUND)
            menu_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddCategoryByMenu(APIView):
    def post(self, request):
        if is_access(request):
            serializer = CategoryAddSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        if is_access(request):
            try:
                category_instance = MenuCategory.objects.get(pk=pk)
            except MenuCategory.DoesNotExist:
                return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CategoryAddSerializer(category_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk):
        if is_access_category_pk(request, pk):
            list = MenuCategory.objects.get(pk=pk)
            return Response(
                {
                    'category': CategoryAddSerializer(list, many=False).data
                }
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if is_access_category_pk(request, pk):
            try:
                category_instance = MenuCategory.objects.get(pk=pk)
            except MenuCategory.DoesNotExist:
                return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)

            category_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddProductByCategory(APIView):
    def post(self, request):
        if is_access(request):
            serializer = ProductAddSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if is_access(request):
            try:
                product_instance = Products.objects.get(pk=pk)
            except Products.DoesNotExist:
                return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductAddSerializer(product_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        if is_access_product_pk(request, pk):
            list = Products.objects.get(pk=pk)
            return Response(
                {
                    'product': ProductAddSerializer(list, many=False).data
                }
            )
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        if is_access_product_pk(request, pk):
            try:
                product_instance = Products.objects.get(pk=pk)
            except Products.DoesNotExist:
                return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

            product_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateProductSorting(APIView):
    def put(self, request):
        data = request.data
        for item in data:
            if is_access_product_pk(request, item.get('id')):
                product_id = item.get('id')
                sorting_number = item.get('sorting_number')
                try:
                    product = Products.objects.get(pk=product_id)
                    product.sorting_number = sorting_number
                    product.save()
                except Products.DoesNotExist:
                    pass
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Products sorting updated successfully'}, status=status.HTTP_200_OK)


class UpdateCategorySorting(APIView):
    def put(self, request):
        data = request.data
        for item in data:
            if is_access_category_pk(request, item.get('id')):
                product_id = item.get('id')
                sorting_number = item.get('sorting_number')
                try:
                    category = MenuCategory.objects.get(pk=product_id)
                    category.sorting_number = sorting_number
                    category.save()
                except MenuCategory.DoesNotExist:
                    pass
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Category sorting updated successfully'}, status=status.HTTP_200_OK)


class GetProductsByIds(APIView):
    def post(self, request):
        product_data = request.data
        products_with_count = []
        for data in product_data:
            try:
                product_id = data['id']
                product = Products.objects.get(id=product_id)
                count = data.get('count', 0)
                product.count = count
                products_with_count.append(product)
            except Products.DoesNotExist:
                pass
        serializer = ProductWithCountSerializer(products_with_count, many=True)
        return Response(serializer.data)
