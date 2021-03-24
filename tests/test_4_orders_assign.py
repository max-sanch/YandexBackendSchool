import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests import data


class OrdersAssignTests(APITestCase):
	def test_1_normal_assign(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.post(
			reverse('create_orders'),
			data.normal_create_orders,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 1},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			json.loads(response.content).get('orders'),
			[{'id': 3}, {'id': 2}]
		)

		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 4},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			json.loads(response.content).get('orders'),
			[{'id': 1}, {'id': 5}]
		)

	def test_2_normal_assign(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.post(
			reverse('create_orders'),
			data.normal_create_orders,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 5},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			json.loads(response.content).get('orders'),
			[{'id': 8}, {'id': 2}]
		)
		assign_time = json.loads(response.content).get('assign_time')

		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 1},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 5},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			json.loads(response.content),
			{'orders': [{'id': 8}, {'id': 2}], 'assign_time': assign_time}
		)

	def test_3_normal_assign(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 1},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(json.loads(response.content), {'orders': []})

	def test_4_fail_assign(self):
		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 1},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(
			json.loads(response.content),
			{'courier_id': {'not_found': 'Курьер с таким идентификатором не найден.'}}
		)

	def test_5_fail_assign(self):
		response = self.client.post(
			reverse('assign_order'),
			{},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'courier_id': ['Обязательное поле.']})

	def test_6_fail_assign(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 1, 'order_id': 1},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'fields': ['Получены неописанные поля: order_id.']})

	def test_7_fail_assign(self):
		response = self.client.post(
			reverse('assign_order'),
			{'courier_id': 'Первый'},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'courier_id': ['Введите правильное число.']})
