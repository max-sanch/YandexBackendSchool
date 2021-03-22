from rest_framework import serializers
import core.validators as validator


class CreateDataListSerializer(serializers.Serializer):
	"""Сериализатор тела запроса списка данных"""

	data = serializers.ListField(
		label='Промежутки приёма заказов',
		allow_empty=False,
		child=serializers.JSONField()
	)

	class Meta:
		fields = ('data', )
		validators = [validator.ValidationEmpty(), validator.ValidationFields()]
