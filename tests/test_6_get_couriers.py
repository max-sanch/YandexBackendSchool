import json
from datetime import timedelta, datetime

from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from tests import data


class GetCourierTests(APITestCase):
	def test_1_normal_get(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.get(reverse('one_courier', args=[1]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			json.loads(response.content),
			{
				'courier_id': 1,
				'courier_type': 'foot',
				'regions': [1, 12, 22],
				'working_hours': ['11:35-14:05', '09:00-11:00'],
				'earnings': 0
			}
		)

	def test_2_normal_get(self):
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
		assign_time = datetime.strptime(json.loads(response.content).get('assign_time'), settings.TIME_FORMAT)
		complete_time = assign_time + timedelta(minutes=10)

		response = self.client.post(
			reverse('complete_order'),
			{
				'courier_id': 1,
				'order_id': 2,
				'complete_time': complete_time.strftime(settings.TIME_FORMAT),
			},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		response = self.client.get(reverse('one_courier', args=[1]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			json.loads(response.content),
			{
				'courier_id': 1,
				'courier_type': 'foot',
				'regions': [1, 12, 22],
				'working_hours': ['11:35-14:05', '09:00-11:00'],
				'earnings': 1000,
				'rating': 4.17
			}
		)

	def test_3_fail_get(self):
		response = self.client.get(reverse('one_courier', args=[1]))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
