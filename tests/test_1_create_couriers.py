import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from couriers.models import Courier
from tests import data


class CreateCouriersTests(APITestCase):
	def test_1_normal_create(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(
			json.loads(response.content),
			{'couriers': [{'id': x} for x in range(1, 6)]}
		)
		self.assertEqual(Courier.objects.count(), 5)
		self.assertEqual(Courier.objects.get(courier_id=1).courier_type, 'foot')
		self.assertEqual(Courier.objects.get(courier_id=2).working_hours, ['09:00-18:00'])
		self.assertEqual(Courier.objects.get(courier_id=5).regions, [1, 12])

	def test_2_fail_create(self):
		response = self.client.post(
			reverse('create_couriers'),
			{},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'data': ['Обязательное поле.']})

	def test_3_fail_create(self):
		response = self.client.post(
			reverse('create_couriers'),
			{'data': []},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'data': ['Этот список не может быть пустым.']})

	def test_4_fail_create(self):
		response = self.client.post(
			reverse('create_couriers'),
			{'data': [{}], 'test': 1},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'fields': ['Получены неописанные поля: test.']})

	def test_5_fail_create(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.fail_create_couriers_data,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(
			json.loads(response.content),
			data.fail_create_couriers_error
		)
