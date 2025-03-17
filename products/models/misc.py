from django.utils import timezone
from django.db import models
from .order import Product

from django.contrib.auth import get_user_model
User = get_user_model()


class Review(models.Model):    #  qoldirilgan sharhlar
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.PositiveIntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}-{self.rating}"


class FlashSale(models.Model):     #   chegirmalar
    product = models.OneToOneField(Product, on_delete=models.CASCADE, db_index=True)  # search vs filter
    discount_percentage = models.PositiveIntegerField()      # qo'yiladigan chegirma foizi
    start_time = models.DateTimeField()   # search vs filter
    end_time = models.DateTimeField()

    def is_active(self):
        time = timezone.now()
        return self.start_time <= time <= self.end_time

    class Meta:
        unique_together = ('product', 'start_time', 'end_time')   #  3 tasi ham bir xil bo'lishiga yo'l qo'ymaydi


class ProductViewHistory(models.Model):    #  userlar productni ko'rganini qayt etadi
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
