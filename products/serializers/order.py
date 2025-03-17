from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from products.models import Order, Product


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'quantity', 'created_at', 'total_price', 'phone_number', 'is_paid']

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

    def validate_quantity(self, value):
        try:

            product_id = self.initial_data['product']
            product = Product.objects.get(id=product_id)

            if value > product.stock:
                raise serializers.ValidationError("Not enough items in stock")

            elif value < 1:
                raise serializers.ValidationError("quantity must be greater than 0")

            return value
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Product not found")

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        product = order.product
        product.stock -= order.quantity
        product.save()
        self.send_confirmation_email()
        return order

    def send_confirmation_email(self):
        print(f"Sent confirmation email for order")



