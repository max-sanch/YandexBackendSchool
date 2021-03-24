import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from couriers.models import Courier
from tests import data


class UpdateCouriersTests(APITestCase):
	def test_1_normal_update(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Courier.objects.get(courier_id=1).courier_type, 'foot')

		response = self.client.patch(
			reverse('one_courier', args=[1]),
			{'courier_type': 'car'},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Courier.objects.get(courier_id=1).courier_type, 'car')

	def test_2_normal_update(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Courier.objects.get(courier_id=2).working_hours, ['09:00-18:00'])

		response = self.client.patch(
			reverse('one_courier', args=[2]),
			{'working_hours': ['09:00-11:00']},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Courier.objects.get(courier_id=2).working_hours, ['09:00-11:00'])

	def test_3_normal_update(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Courier.objects.get(courier_id=5).regions, [1, 12])
		self.assertEqual(Courier.objects.get(courier_id=5).courier_type, 'foot')

		response = self.client.patch(
			reverse('one_courier', args=[5]),
			{'regions': [23], 'courier_type': 'bike'},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Courier.objects.get(courier_id=5).regions, [23])
		self.assertEqual(Courier.objects.get(courier_id=5).courier_type, 'bike')

	def test_4_fail_update(self):
		response = self.client.patch(
			reverse('one_courier', args=[1]),
			{'courier_type': 'bike'},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(json.loads(response.content), {'detail': 'Страница не найдена.'})

	def test_5_fail_update(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.patch(
			reverse('one_courier', args=[1]),
			{},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'empty_data': ['Запрос не должен быть пустым.']})

	def test_6_fail_update(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.patch(
			reverse('one_courier', args=[1]),
			{'data': []},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'fields': ['Получены неописанные поля: data.']})

	def test_7_fail_update(self):
		response = self.client.post(
			reverse('create_couriers'),
			data.normal_create_couriers,
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		response = self.client.patch(
			reverse('one_courier', args=[1]),
			{'courier_type': 'bus'},
			format='json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(json.loads(response.content), {'courier_type': ['Значения bus нет среди допустимых вариантов.']})
