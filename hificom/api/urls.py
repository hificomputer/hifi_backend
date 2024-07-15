from django.urls import path
from hificom.api import views

urlpatterns = [
    path('categories/', views.CategoriesView.as_view(), name="categories"),
    path('categories/<str:slug>/', views.ViewCategory.as_view(), name="view_category"),
    path('categories/<str:slug>/groups/', views.CategoryGroupsView.as_view(), name="view_category_groups"), # slug of root
    path('categories/<str:slug>/tables/update/', views.update_tables, name="update_tables"),
    path('categories/<str:slug>/products/', views.CategoryProductsView.as_view(), name="category_products"),
    path('categories/<str:slug>/allproducts/', views.AllProductsSemiDetailView.as_view(), name="all_products_full"),
    path('t/<str:slug>/products/', views.TaggedProductsView.as_view(), name="tagged_products"),
    path('categories/<str:slug>/addproduct/', views.add_product, name="add_product"),
]
