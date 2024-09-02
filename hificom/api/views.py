from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, 
                                     DestroyAPIView, 
                                     ListAPIView, 
                                     ListCreateAPIView, 
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import json
from hificom.models import (Carousel,
                            Cart,
                            Category, 
                            CategoryGroup,
                            Coupon,
                            KeyFeature,
                            Order,
                            Product,
                            ProductCollection,
                            SpecificationTable,
                            WishList)

from .serializer import (CarouselSerializer,
                         CategoryDetailSerializer, 
                         CategoryGroupSerializer,
                         CategorySerializer,
                         KeyFeatureSerializer,
                         OrderSerializer,
                         ProductBasicSerializer,
                         ProductCollectionSerializer,
                         ProductCreateSerializer,
                         ProductDetailSerializer,
                         ProductSemiDetailSerializer,
                         SpecTableSerializer,
                         WishlistSerializer)


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
        parent_in_tree_of = self.request.GET.get('treeof', 'null')
        categories = Category.objects.all()
        if cat_type != 'all':
            categories = categories.filter(cat_type=cat_type)
        if parent == 'null' and parent_in_tree_of == 'null':
            categories = categories.filter(parent=None)
        elif parent == 'null' and parent_in_tree_of != 'null':
            tree_of = get_object_or_404(
                Category,
                Q(pk=parent_in_tree_of) | Q(slug=parent_in_tree_of) if parent_in_tree_of.isdigit() 
                else Q(slug=parent_in_tree_of)
            )
            categories = categories.filter(parent__in=tree_of.category_tree)
        elif parent != 'null' and parent != 'all':
            categories = categories.filter(
                Q(parent__pk=parent) | Q(parent__slug=parent) if parent.isdigit()
                else Q(parent__slug=parent)
            )
        return categories


class CategoryGroupsView(ListAPIView):
    serializer_class = CategoryGroupSerializer

    def get_queryset(self):
        root_cat = utils.get_category_from_identifier(self.kwargs.get('identifier'))
        return CategoryGroup.objects.filter(root__in=root_cat.category_tree)


class ViewCategory(RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()

    def get_object(self):
        return utils.get_category_from_identifier(self.kwargs.get('identifier'))


class CategorTablesView(ListAPIView):
    serializer_class = SpecTableSerializer

    def get_object(self):
        return utils.get_category_from_identifier(self.kwargs.get('identifier'))
    
    def get_queryset(self):
        category = self.get_object()
        if self.request.GET.get('tree'):
            return SpecificationTable.objects.filter(category__in=category.category_tree)
        else:
            category.specificationtable_set.all()


class CategoryUnpaginatedProductsView(ListAPIView):
    serializer_class = ProductBasicSerializer

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs.get('slug'))


class CategoryProductsView(CategoryUnpaginatedProductsView):
    pagination_class = ProductsPagination


class TaggedProductsUnpaginatedView(ListAPIView):
    serializer_class = ProductBasicSerializer
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Product.objects.filter(Q(category__slug=slug) | Q(tags__slug=slug)).distinct()


class TaggedProductsView(TaggedProductsUnpaginatedView):
    pagination_class = ProductsPagination


class SearchProduct(ListAPIView):
    serializer_class = ProductBasicSerializer

    def get_queryset(self):
        query = self.request.GET.get('query')
        products = Product.objects.filter(Q(title__icontains=query))
        return products


class AllProductsSemiDetailView(ListAPIView):
    serializer_class = ProductSemiDetailSerializer
    pagination_class = ProductsPagination
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return utils.filter_products(slug, self.request)


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'


class ProductKeyFeaturesView(ListAPIView):
    serializer_class = KeyFeatureSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return KeyFeature.objects.filter(product__slug=slug)
    

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


class ConfirmOrder(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        cart = get_object_or_404(Cart, cartid=data.pop('cartid'))
        item_count, payable = cart.cart_total()
        payable += utils.get_shipping_charges(item_count, data['location'])
        coupon_code = data.get('coupon')
        if coupon := Coupon.objects.filter(code=coupon_code).first():
            payable -= utils.get_coupon_discount_amount(cart, coupon)
            data['coupon'] = coupon.id
        data['payable'] = payable
        data['cart'] = cart.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        utils.update_cart_checked_out(cart, request)
        return Response(serializer.data)


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
    return Response('added')


@api_view(['POST'])
@permission_classes([IsAdmin])
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = json.loads(request.data['json'])
    data['prev_images'] = data.pop('images')
    data['images'] = request.FILES.getlist('new_images')
    serializer = ProductCreateSerializer(product, data=data)
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as e:
            return Response({'detail': f'Cannot edit product. Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'category': product.category.slug})


@api_view(['POST'])
@permission_classes([IsAdmin])
def alter_stock_status(request, pk):
    product = get_object_or_404(Product, pk=pk)
    stock_status = request.data.get('in_stock')
    if type(stock_status) == bool:
        product.in_stock = stock_status
        product.save()
        return Response({'in_stock': product.in_stock})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
    cartinfo = request.data.get('cartinfo')
    utils.update_cart(cart, cartinfo)
    products = [cartprod.product for cartprod in cart.cartproduct_set.all()]
    data = {'cartid': cart.cartid, 'prod_data': []}
    if products:
        serializer = ProductBasicSerializer(products, many=True, context={'request': request})
        data['prod_data'] = serializer.data
    data['total_items'], data['total_amount'] = cart.cart_total()
    return Response(data)


@api_view(['POST'])
def apply_coupon(request):
    coupon = get_object_or_404(Coupon, code=request.data.get('coupon'))
    cart = get_object_or_404(Cart, cartid=request.data.get('cartid'))
    try:
        discount_amount = utils.get_coupon_discount_amount(cart, coupon)
    except ValidationError as e:
        return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'discount': discount_amount})


@api_view(['POST'])
def sync_wishlist(request):
    wlist = utils.perform_wishlist_sync(request)
    return Response(WishlistSerializer(wlist).data)
