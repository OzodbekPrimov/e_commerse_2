from .servises.flash_sale import FlashSaleListCreateView, check_flash_sale
from .servises.product_view_history import ProductViewHistoryCreate
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .servises.order_views import OrderListRetrieveView, top_selling_products, OrderCreateView
from .views import ProductViewsSet, CategoryViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r"products", ProductViewsSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sale/', FlashSaleListCreateView.as_view(), name='sale'),
    path('check-sale/<int:product_id>/', check_flash_sale, name='check_sale' ),
    path('product-view/', ProductViewHistoryCreate.as_view(), name='product-view-history-create'),
    path('top-order-product/', top_selling_products, name='top_order_product'),
    path('orders/', OrderListRetrieveView.as_view(), name='order-list'),
    path('orders-create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderListRetrieveView.as_view(), name='order-detail'),
]
