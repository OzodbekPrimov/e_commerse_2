from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import FlashSale, ProductViewHistory, Product
from rest_framework import generics, serializers, status
from django_filters import rest_framework as django_filters
from rest_framework import filters
from products.filters import FlashSaleFilter
from rest_framework.pagination import  PageNumberPagination
from products.permissions import IsStaffOrReadOnly


class CustomFlashsalePagination(PageNumberPagination):
    page_size = 2


class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = '__all__'

    serializer_class = FlashSaleSerializer
    pagination_class = CustomFlashsalePagination
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = FlashSaleFilter
    search_fields = ['product__name']


@api_view(['get'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error':"Product not fount"}, status=status.HTTP_404_NOT_FOUND)

    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()

    yaqinlashayotgan_chegirmalar = FlashSale.objects.filter(
        product=product,
        start_time__lte=datetime.now() + timedelta(hours=24)
    ).first()

    if user_viewed and yaqinlashayotgan_chegirmalar:
        discount = yaqinlashayotgan_chegirmalar.discount_percentage
        start_time = yaqinlashayotgan_chegirmalar.start_time
        end_time = yaqinlashayotgan_chegirmalar.end_time
        return Response({
            'message':f"bu mahsulotga yaqinda {discount}% chegirma bo'ladi",
            'start_time': start_time,
            'end_time':end_time
        })
    else:
        return Response({
            "message":"Bu mahsulotga yaqin orada chegirma yo'q"
        })



