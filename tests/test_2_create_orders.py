import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order
from tests import data


class CreateOrdersTests(APITestCase):
	def test_1_normal_create(self):
		response = self.client.post(
			reverse('create_orders'),
			data.normal_create_orders,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(
			json.loads(response.content),
			{'orders': [{'id': x} for x in range(1, 11)]}
		)
		self.assertEqual(Order.objects.count(), 10)
		self.assertEqual(Order.objects.get(order_id=1).weight, 0.23)
		self.assertEqual(Order.objects.get(order_id=2).region, 1)
		self.assertEqual(Order.objects.get(order_id=5).delivery_hours, ["09:00-12:00", "13:00-18:00"])
		self.assertEqual(Order.objects.get(order_id=10).weight, 8)

	def test_2_fail_create(self):
		response = self.client.post(
			reverse('create_orders'),
			{},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'data': ['Обязательное поле.']})

	def test_3_fail_create(self):
		response = self.client.post(
			reverse('create_orders'),
			{'data': []},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'data': ['Этот список не может быть пустым.']})

	def test_4_fail_create(self):
		response = self.client.post(
			reverse('create_orders'),
			{'data': [{}], 'test': 1},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'fields': ['Получены неописанные поля: test.']})

	def test_5_fail_create(self):
		response = self.client.post(
			reverse('create_orders'),
			data.fail_create_orders_data,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(
			json.loads(response.content),
			data.fail_create_orders_error
		)
