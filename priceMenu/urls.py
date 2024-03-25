from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from establishment.views import *
from userProfile.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('establishment/<int:establishment_id>/information/', EstablishmentAllListView.as_view()),
    path('establishment/<int:establishment_id>/products/', ListOfProducts.as_view()),
    path('establishment/<int:establishment_id>/promotions/', GetPromotionsByEstablishment.as_view()),
    path('dict/<int:establishment_id>/menu/', GetMenuListByEstablishment.as_view()),
    path('dict/<int:menu_id>/category/', GetCategoryListByMenuId.as_view()),
    path('dict/<int:category_id>/products/', GetProductListByCategoryId.as_view()),
    path('dict/<int:product_id>/product/information/', GetProductById.as_view()),
    path('add_edit/menu/establishment/<int:pk>/', AddMenuByEstablishment.as_view()),
    path('add_edit/menu/establishment/', AddMenuByEstablishment.as_view()),
    path('add_edit/category/<int:pk>/', AddCategoryByMenu.as_view()),
    path('add_edit/category/', AddCategoryByMenu.as_view()),
    path('add_edit/products/<int:pk>/', AddProductByCategory.as_view()),
    path('add_edit/products/', AddProductByCategory.as_view()),
    path('add_edit/products/sorting/', UpdateProductSorting.as_view()),
    path('add_edit/categories/sorting/', UpdateCategorySorting.as_view()),
    path('product/get_list/', GetProductsByIds.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/token/check/', TokenCheck.as_view()),
    path('auth/token/get_establishment/', GetEstablishmentByToken.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
