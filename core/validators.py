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
