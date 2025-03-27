from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

from products.models import Category, Product, Review


class ProductViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='+998507556306', password='root')
        self.staff_user = User.objects.create_user(phone_number='+998772100532', password='ozodbek2006', is_staff=True)

        self.category1 = Category.objects.create(name='Ichimliklar')
        self.category2 = Category.objects.create(name='Kombolar')

        self.product1 = Product.objects.create(name='Fanta', description='test product1', price='15000', category=self.category1)
        self.product2 = Product.objects.create(name='Iftor kombo', description='test product2', price='40000', category=self.category2)

        Review.objects.create(user_id=1, product=self.product1, rating=4)
        Review.objects.create(user_id=2, product=self.product2, rating=3)
        Review.objects.create(user_id=1, product=self.product1, rating=3)

    def test_product_list(self):
        url = reverse('product-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_product_detail(self):
        url = reverse('product-detail', args=[self.product1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)  # response data da nimalar kelishini bilib olish uchun
        self.assertEqual(response.data['product']['name'], 'Fanta')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_rated(self):
        url = reverse('product-top-rated')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[1]['name'], 'Iftor kombo')

    def test_average_rating(self):
        url = reverse('product-average-rating', args=[self.product1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        # print(response.data)
        self.assertEqual(response.data['average_rating'], 3.5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_denied_for_anonymous_create(self):
        self.client.force_authenticate(user=None)
        url = reverse('product-list')
        data = {'name':'Test product', 'price':1000, 'category':self.category1.id}
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_granted_for_staff(self):
        self.client.force_authenticate(self.staff_user)
        url = reverse('product-list')
        # print(url)
        data = {'name':'Test kombo', 'price':30000, 'category':self.category2.id, 'description':'This is test product description'}
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)