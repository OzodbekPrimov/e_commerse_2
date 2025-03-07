
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from products.serializers import OrderSerializer
from products.models import Order

from products.filters import OrderFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi

class CustomOrderPagination(PageNumberPagination):
    page_size = 2

class OrderListRetrieveView(APIView):
    pagination_class = CustomOrderPagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class =OrderFilter
    search_fields = ['product__name']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'order_status', openapi.IN_QUERY, description='Order status (e.g., pending, completed)',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'start_date', openapi.IN_QUERY, description='Start date (greater than or equal)',
                type=openapi.TYPE_STRING, format='date-time'
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY, description='End date (less than or equal)',
                type=openapi.TYPE_STRING, format='date-time'
            ),
            openapi.Parameter(
                'min_quantity', openapi.IN_QUERY, description='Minimum quantity', type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_quantity', openapi.IN_QUERY, description='Maximum quantity', type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'page', openapi.IN_QUERY, description='Page number for pagination', type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get(self, request, pk=None):
        if pk:
            try:
                order = Order.objects.get(pk=pk)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({'detail':'Not Fount'}, status=HTTP_404_NOT_FOUND)
        else:
            queryset = Order.objects.all()
            for backend in self.filter_backends:
                if hasattr(backend, 'filter_queryset'):
                    queryset = backend().filter_queryset(request, queryset, self)

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)

            serializer = OrderSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)


class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def top_selling_products(request):
    # TOP 3 mahsulotlarni jami sotilgan miqdori bo‘yicha tartiblab olish
    top_products = (
        Order.objects
        .values('product__name')  # Dictionary formatida qaytadi
        .annotate(total_quantity=Sum('quantity'))  # Jami sotilgan so‘rovni tayyorlash
        .order_by('-total_quantity')[:2]  # Top 3 mahsulotni tanlash
    )

    # Agar mahsulotlar bo'lmasa
    if not top_products:
        return Response({"message": "Mahsulotlar mavjud emas"}, status=HTTP_200_OK)

    # Qaytgan natijalarni JSON ko‘rinishga aylantirish
    return Response(list(top_products), status=HTTP_200_OK)


