from rest_framework.test import APITestCase

from products.models import Category
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class CategoryTest(APITestCase):
    # python manage.py dumpdata products.Category --format=yaml --indent=4 > products/fixtures/categories.yaml
    fixtures = ['categories']

    def setUp(self):
        self.user = User.objects.create_user(phone_number='+998940075950')
        self.staff_user = User.objects.create_user(phone_number='+998772100532', is_staff=True)

        self.client.force_authenticate(self.user)
        self.category1 = Category.objects.first()
        self.category3 = Category.objects.get(id=3)

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        # print(response.data)  # data da nima qaytishiga qarab shart beramiz
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail(self):
        url = reverse('category-detail', args=[self.category1.id])
        response = self.client.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Lavashlar")

    def test_category_create(self):
        url = reverse('category-list')
        data = {'name':'shirinliklar'}
        self.client.force_authenticate(self.staff_user)
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_update(self):
        self.client.force_authenticate(self.staff_user)
        url = reverse('category-detail', args=[self.category3.pk])
        data = {'name':'Ichimliklar'}
        response = self.client.put(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(Category.objects.get(id=3)), 'Ichimliklar')

    def test_category_delete(self):
        self.client.force_authenticate(self.staff_user)
        url = reverse('category-detail', args=[self.category1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


