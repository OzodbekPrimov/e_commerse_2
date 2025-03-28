from . import signals

from .servises.flash_sale import FlashSaleListCreateView, check_flash_sale
from .servises.product_view_history import ProductViewHistoryCreate
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewset, CategoryViewSet, ReviewViewSet, OrderViewSet, top_selling_products
from .servises.replanish_stock import admin_replenish_stock


router = DefaultRouter()
router.register(r"products", ProductViewset)
router.register(r"reviews", ReviewViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('sale/', FlashSaleListCreateView.as_view(), name='sale'),
    path('check-sale/<int:product_id>/', check_flash_sale, name='check_sale' ),
    path('product-view/', ProductViewHistoryCreate.as_view(), name='product-view-history-create'),
    path('top-order-product/', top_selling_products, name='top_order_product'),

    path('admin/replenish_stock/<int:product_id>/<int:amount>', admin_replenish_stock, name='admin_replenish_stock'),
]
