
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from rest_framework import viewsets

from products.permissions import IsOwnerReadOnly
from products.serializers import OrderSerializer
from products.models import Order

from products.filters import OrderFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomOrderPagination(PageNumberPagination):
    page_size = 2


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer', 'product').only('id', 'customer', 'product', 'quantity',
                                                                        'created_at', 'status')
    serializer_class = OrderSerializer

    pagination_class = CustomOrderPagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = OrderFilter
    search_fields = ['product__name']
    permission_classes = [IsOwnerReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'customer', openapi.IN_QUERY, description='Customer ID to filter orders', type=openapi.TYPE_INTEGER
            ),
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
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('customer', None)
        if user_id:
            try:
                user_id = int(user_id)
                # self.queryset ni o'zgartirish o'rniga yangi queryset ishlatamiz
                queryset = self.get_queryset().filter(customer_id=user_id)
            except (ValueError, TypeError):
                raise ValidationError("User not found")  # Xato xabarini aniqlashtirish
        else:
            queryset = self.get_queryset()

        # Filter backends va paginationni qo'llash
        queryset = self.filter_queryset(queryset)
        return super().list(request, *args, **kwargs)


@api_view(['GET'])
def top_selling_products(request):
    permission_classes(IsOwnerReadOnly)  #  faqat adminlar ko'ra oladi
    # TOP 2 mahsulotlarni jami sotilgan miqdori bo‘yicha tartiblab olish
    top_products = (
        Order.objects
        .values('product__name')  # Dictionary formatida qaytadi
        .annotate(total_quantity=Sum('quantity'))  # Jami sotilgan so‘rovni tayyorlash
        .order_by('-total_quantity')[:2]  # Top 2 mahsulotni tanlash
    )

    # Agar mahsulotlar bo'lmasa
    if not top_products:
        return Response({"message": "Mahsulotlar mavjud emas"}, status=HTTP_200_OK)

    # Qaytgan natijalarni JSON ko‘rinishga aylantirish
    return Response(list(top_products), status=HTTP_200_OK)


