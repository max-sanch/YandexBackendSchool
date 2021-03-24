import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests import data


class OrdersCompleteTests(APITestCase):
	def test_1_normal_complete(self):
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

		response = self.client.post(
			reverse('complete_order'),
			{
				'courier_id': 1,
				'order_id': 2,
				'complete_time': '2021-01-10T10:33:01Z',
			},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(json.loads(response.content), {'order_id': 2})

		response = self.client.post(
			reverse('complete_order'),
			{
				'courier_id': 1,
				'order_id': 3,
				'complete_time': '2021-01-10T10:33:01Z',
			},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		response = self.client.post(
			reverse('complete_order'),
			{
				'courier_id': 1,
				'order_id': 2,
				'complete_time': '2021-01-10T10:33:01Z',
			},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(json.loads(response.content), {'order_id': 2})

	def test_2_fail_complete(self):
		response = self.client.post(
			reverse('complete_order'),
			{},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(
			json.loads(response.content),
			{
				'courier_id': ['Обязательное поле.'],
				'order_id': ['Обязательное поле.'],
				'complete_time': ['Обязательное поле.']
			}
		)

	def test_3_fail_complete(self):
		response = self.client.post(
			reverse('complete_order'),
			{
				'courier_id': 1,
				'order_id': 1,
				'complete_time': '2021-01-10T10:33:01Z',
			},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(
			json.loads(response.content),
			{
				'courier_id': {'not_found': 'Курьер с таким идентификатором не найден.'},
				'order_id': {'not_found': 'Заказ с таким идентификатором не найден.'}
			}
		)

	def test_4_fail_complete(self):
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
			reverse('complete_order'),
			{
				'courier_id': 1,
				'order_id': 1,
				'complete_time': '2021-01-10T10:33:01Z',
			},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(
			json.loads(response.content),
			{'belongs_courier': ['Заказ не принадлежит курьеру.']}
		)

	def test_5_fail_complete(self):
		response = self.client.post(
			reverse('complete_order'),
			{
				'courier_id': 'Первый',
				'order_id': 1,
				'complete_time': '2021-01-10T10:33:01Z',
			},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(
			json.loads(response.content),
			{
				'courier_id': ['Введите правильное число.'],
				'order_id': {'not_found': 'Заказ с таким идентификатором не найден.'}
			}
		)
