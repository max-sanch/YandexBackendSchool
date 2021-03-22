from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings

from .models import Order, OrderDetail
from couriers.models import Courier
import core.validators as validator


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
		validators=[validator.ValidationTimeFormat()]
	)

	class Meta:
		model = Order
		exclude = ('status', )
		validators = [validator.ValidationFields()]


class OrderAssignSerializer(serializers.ModelSerializer):
	"""Формирование группы заказов для курьера"""

	courier_id = serializers.IntegerField(
		label='Идентификатор курьера',
		min_value=0,
		max_value=2147483647,
		validators=[validator.ValidationCourierID(Courier)]
	)

	class Meta:
		model = Courier
		fields = ('courier_id', )
		validators = [validator.ValidationEmpty(), validator.ValidationFields()]


class OrderCompleteSerializer(serializers.Serializer):
	"""Завершение заказа"""

	courier_id = serializers.IntegerField(
		label='Идентификатор курьера',
		min_value=0,
		max_value=2147483647,
		validators=[validator.ValidationCourierID(Courier)]
	)
	order_id = serializers.IntegerField(
		label='Идентификатор заказа',
		min_value=0,
		max_value=2147483647,
		validators=[validator.ValidationOrderID(Order)]
	)
	complete_time = serializers.DateTimeField(
		format=settings.TIME_FORMAT
	)

	class Meta:
		fields = ('courier_id', 'order_id', 'complete_time')
		validators = [
			validator.ValidationEmpty(),
			validator.ValidationFields(),
			validator.ValidationOrderBelongsCourier(Courier, Order, OrderDetail)
		]
