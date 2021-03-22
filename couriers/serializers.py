from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Courier
import core.validators as validator


class CourierCreateSerializer(serializers.ModelSerializer):
	"""Добавление курьера"""

	courier_id = serializers.IntegerField(
		label='Идентификатор курьера',
		min_value=0,
		max_value=2147483647,
		validators=[UniqueValidator(queryset=Courier.objects.all())]
	)
	courier_type = serializers.ChoiceField(
		choices=Courier.COURIER_TYPES,
		label='Тип курьера'
	)
	regions = serializers.ListField(
		allow_empty=True,
		child=serializers.IntegerField(
			label='Идентификатор района',
			min_value=0,
			max_value=2147483647
		),
		label='Список идентификаторов районов'
	)
	working_hours = serializers.ListField(
		allow_empty=True,
		child=serializers.CharField(
			label='Период работы курьера',
			max_length=11
		),
		label='График работы курьера',
		validators=[validator.ValidationTimeFormat()]
	)

	class Meta:
		model = Courier
		exclude = ('id', )
		validators = [validator.ValidationFields()]


class CourierUpdateSerializer(serializers.ModelSerializer):
	"""Частичное изменение курьера"""

	courier_type = serializers.ChoiceField(
		choices=Courier.COURIER_TYPES,
		label='Тип курьера'
	)
	regions = serializers.ListField(
		allow_empty=True,
		child=serializers.IntegerField(
			label='Идентификатор района',
			min_value=0,
			max_value=2147483647
		),
		label='Список идентификаторов районов'
	)
	working_hours = serializers.ListField(
		allow_empty=True,
		child=serializers.CharField(
			label='Период работы курьера',
			max_length=11
		),
		label='График работы курьера',
		validators=[validator.ValidationTimeFormat()]
	)

	class Meta:
		model = Courier
		exclude = ('id', 'courier_id')
		validators = [validator.ValidationEmpty(), validator.ValidationFields()]
