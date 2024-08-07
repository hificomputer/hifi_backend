from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth import get_user_model
import json
from hificom.models import (Category, 
                            CategoryGroup, 
                            Product,
                            ProductCollection,
                            Carousel)

from .serializer import (CategorySerializer, 
                         CategoryDetailSerializer, 
                         ProductSemiDetailSerializer,
                         CategoryGroupSerializer,
                         ProductBasicSerializer,
                         ProductDetailSerializer,
                         ProductCreateSerializer,
                         CarouselSerializer,
                         ProductCollectionSerializer)

from .permission import IsAdminOrReadOnly, IsAdmin
from .pagination import ProductsPagination
from . import utils
User = get_user_model()


@api_view()
def user_homepage(request):
    data = {
        'carousels': CarouselSerializer(
            Carousel.objects.all()[:10],
            many=True,
            context={'request': request}
        ).data,
        'collections': ProductCollectionSerializer(
            ProductCollection.objects.all(),
            many=True,
            context={'request': request}
        ).data,
    }
    return Response(data)


class CategoriesView(ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        cat_type = self.request.GET.get('type', 'all')
        parent= self.request.GET.get('parent', 'null')
        categories = Category.objects.all()
        if cat_type != 'all':
            categories = categories.filter(cat_type=cat_type)
        if parent == 'null':
            categories = categories.filter(parent=None)
        elif parent != 'null' and  parent.isdigit():
            parent_id = int(parent)
            categories = categories.filter(parent__id=parent_id)
        return categories

class CategoryGroupsView(ListAPIView):
    serializer_class = CategoryGroupSerializer

    def get_queryset(self):
        root_slug = self.kwargs.get('slug')
        root_cat = get_object_or_404(Category, slug=root_slug)
        return CategoryGroup.objects.filter(root__in=root_cat.category_tree)


class ViewCategory(RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs.get('slug'))

class CategoryProductsView(ListAPIView):
    serializer_class = ProductBasicSerializer
    pagination_class = ProductsPagination

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs.get('slug'))


class TaggedProductsView(ListAPIView):
    serializer_class = ProductBasicSerializer
    pagination_class = ProductsPagination
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Product.objects.filter(Q(category__slug=slug) | Q(tags__slug=slug)).distinct()


class AllProductsSemiDetailView(ListAPIView):
    serializer_class = ProductSemiDetailSerializer
    pagination_class = ProductsPagination
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return utils.filter_products(slug, self.request)
    
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs.get('slug'))


class RelatedProductsView(ListAPIView):
    serializer_class = ProductBasicSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        prod = get_object_or_404(Product, pk=pk)
        return Product.objects.filter(tags__in=prod.tags.all()).distinct()

 
class DeleteProduct(DestroyAPIView):
    serializer_class = ProductBasicSerializer
    queryset = Product.objects.all()
    permission_classes=[IsAdmin]


@api_view(['POST'])
@permission_classes([IsAdminOrReadOnly])
def update_tables(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    try:
        utils.update_cat_tables(cat, request.data)
    except Exception as e:
        return Response({'detail': f'Error while updating: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    return Response('Updated')


@api_view(['POST'])
@permission_classes([IsAdminOrReadOnly])
def add_product(request, slug):
    data = json.loads(request.data['json'])
    data['images'] = request.FILES.getlist('images')
    serializer = ProductCreateSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as e:
            return Response({'detail': f'Cannot add product. Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response('testing')

@api_view()
@permission_classes([IsAdmin])
def dashboard_stats(request):
    data = {
        'num_products': Product.objects.count(),
        'num_users': User.objects.count(),
        'num_orders': 0,
        'num_messages': 0,
    }
    return Response(data)


@api_view(['POST'])
def get_cart_products(request):
    cart = utils.get_cart(request)
    cartinfo: dict = request.data.get('cartinfo')
    prod_ids = cartinfo.keys()
    data = {'cartid': cart.id}
    if prod_ids:
        products = Product.objects.filter(id__in=prod_ids)
        serializer = ProductBasicSerializer(products, many=True, context={'request': request})
        data['prod_data'] = serializer.data
    return Response(data)