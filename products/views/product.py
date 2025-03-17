from rest_framework import viewsets, filters
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from products.models import Product
from products.permissions import IsStaffOrReadOnly
from products.serializers import ProductSerializer
from django_filters import rest_framework as django_filters
from products.filters import ProductFilter
from rest_framework.response import Response
from django.db.models import Avg

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



class CustomPagination(PageNumberPagination):
    page_size = 3


class ProductViewset(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = CustomPagination

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Category name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'min_price', openapi.IN_QUERY, description="Minimal qiymati",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_price', openapi.IN_QUERY, description='Maximal narxi',
                type=openapi.TYPE_NUMBER
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_product = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializer(related_product, many=True)
        return Response({
            'product':serializer.data,
            'related_products':related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:2]
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        print(reviews)
        if reviews.count()==0:
            return Response({'average_rating':"No reviews yet!"})
        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({"average_rating":avg_rating})








