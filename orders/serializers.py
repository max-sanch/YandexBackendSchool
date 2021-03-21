from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Order, Courier
from core.validators import ValidationFields, ValidationEmpty, ValidationTimeFormat


class OrderCreateSerializer(serializers.ModelSerializer):
	"""Добавление заказа"""

	order_id = serializers.IntegerField(
		label='Идентификатор заказа',
		min_value=0,
		max_value=2147483647,
		validators=[UniqueValidator(queryset=Order.objects.all())]
	)
	weight = serializers.FloatField(
		label='Вес заказа',
		min_value=0.01,
		max_value=50
	)
	region = serializers.IntegerField(
		label='Район доставки заказа',
		min_value=0,
		max_value=2147483647
	)
	delivery_hours = serializers.ListField(
		label='Промежутки приёма заказов',
		allow_empty=False,
		child=serializers.CharField(label='Промежуток приёма заказа', max_length=11),
		validators=[ValidationTimeFormat()]
	)

	class Meta:
		model = Order
		exclude = ('status', )
		validators = [ValidationFields()]


class OrderAssignSerializer(serializers.ModelSerializer):
	"""Формирование группы заказов для курьера"""

	courier_id = serializers.IntegerField(
		label='Идентификатор курьера',
		min_value=0,
		max_value=2147483647
	)

	class Meta:
		model = Courier
		fields = ('courier_id', )
		validators = [ValidationEmpty(), ValidationFields()]

	def validate_courier_id(self, value):
		"""Валидация ID курьера на наличие его в базе"""
		try:
			Courier.objects.get(courier_id=value)
			return value
		except Courier.DoesNotExist:
			raise serializers.ValidationError({'not_found': 'Курьер с таким идентификатором не найден.'})
