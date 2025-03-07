from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


STATUS_CHOISES = [
    ('pending', 'Kutilmoqda'),
    ('shipped', "Jo'natildi"),
    ('delivered', "Yetkazildi")
]


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.PositiveIntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}-{self.rating}"


class FlashSale(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, db_index=True)  # search vs filter
    discount_percentage = models.PositiveIntegerField()      # qo'yiladigan chegirma foizi
    start_time = models.DateTimeField()   # search vs filter
    end_time = models.DateTimeField()

    def is_active(self):
        time = datetime.now()
        return self.start_time <= time <= self.end_time

    class Meta:
        unique_together = ('product', 'start_time', 'end_time')   #  3 tasi ham bir xil bo'lishiga yo'l qo'ymaydi


class ProductViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOISES, default='pending', db_index=True) # filter
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.user.username}-{self.product.name}'


