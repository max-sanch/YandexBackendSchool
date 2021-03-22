import time
from rest_framework import serializers


class ValidationEmpty:
	"""Валидация пустого запроса"""

	requires_context = True

	def __call__(self, data, serializer):
		if len(serializer.initial_data) == 0:
			raise serializers.ValidationError({'empty_data': 'Запрос не должен быть пустым.'})
		return data


class ValidationFields:
	"""Валидация неописанных полей"""

	requires_context = True

	def __call__(self, data, serializer):
		if len(set(serializer.initial_data.keys()) - set(serializer.fields.keys())) != 0:
			raise serializers.ValidationError({
				'fields': 'Получены неописанные поля: %s.' % ', '.join(
					set(serializer.initial_data.keys()) - set(serializer.fields.keys())
				)
			})
		return data


class ValidationTimeFormat:
	"""Валидация формата времени"""

	def __call__(self, value):
		error = {'time_format': 'Неверный формат времени. Нужен: HH:MM-HH:MM'}
		for time_str in value:
			time_list = time_str.split('-')
			if len(time_list) != 2:
				raise serializers.ValidationError(error)
			try:
				time.strptime(time_list[0], '%H:%M')
				time.strptime(time_list[1], '%H:%M')
			except ValueError:
				raise serializers.ValidationError(error)
		return value


class ValidationCourierID:
	"""Валидация ID курьера на наличие его в базе"""

	def __init__(self, courier):
		self.courier = courier

	def __call__(self, value):
		error = {'not_found': 'Курьер с таким идентификатором не найден.'}
		try:
			self.courier.objects.get(courier_id=value)
			return value
		except self.courier.DoesNotExist:
			raise serializers.ValidationError(error)


class ValidationOrderID:
	"""Валидация ID заказа на наличие его в базе"""

	def __init__(self, order):
		self.order = order

	def __call__(self, value):
		error = {'not_found': 'Заказ с таким идентификатором не найден.'}
		try:
			self.order.objects.get(order_id=value)
			return value
		except self.order.DoesNotExist:
			raise serializers.ValidationError(error)


class ValidationOrderBelongsCourier:
	"""Валидация отношения заказа к курьеру"""

	def __init__(self, courier, order, order_detail):
		self.order_detail = order_detail
		self.courier = courier
		self.order = order

	def __call__(self, data):
		error = {'belongs_courier': 'Заказ не принадлежит курьеру.'}
		try:
			order = self.order.objects.get(order_id=data.get('order_id'))
			courier = self.courier.objects.get(courier_id=data.get('courier_id'))
			self.order_detail.objects.get(order=order, courier=courier)
			return data
		except self.order_detail.DoesNotExist:
			raise serializers.ValidationError(error)
