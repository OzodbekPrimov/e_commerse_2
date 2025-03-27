from products.models import Order, Product, Category
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()


class OrderTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='+998940075950', password='rootroot')
        self.staff_user = User.objects.create_user(phone_number='+998772100532', is_staff=True)

        self.category1 = Category.objects.create(name='Lavash')

        self.product1 = Product.objects.create(name='lavash mini', description='test product', price=33000, category=self.category1, stock=34)
        self.product2 = Product.objects.create(name='lavash katta', description='test product', price=40000, category=self.category1, stock=55)

    def test_order_list(self):
        self.client.force_authenticate(self.user)
        url = reverse('order-list')
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_order_detail(self):
        self.client.force_authenticate(self.user)
        url = reverse('order-detail', args=self.order1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
