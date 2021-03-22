from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateDataListSerializer


class CreateDataListMixin:
	"""
	Реализация метода POST на валидацию, обработку ошибок и сохранения
	нескольких объектов представленных в виде json: {"data": []}.
	"""

	def post(self, request, context, serializer_class):
		serialize_data = CreateDataListSerializer(data=request.data)

		# Валидируем основное тело запроса
		if not serialize_data.is_valid():
			return Response(serialize_data.errors, status=status.HTTP_400_BAD_REQUEST)

		errors = {'validation_error': {context+'s': []}}
		valid_objects = []

		# Валидируем список входных данных
		for data in request.data.get('data', []):
			obj = serializer_class(data=data)
			if obj.is_valid():
				valid_objects.append(obj)
			else:
				errors['validation_error'][context+'s'].append({
					'id': obj.initial_data.get(context+'_id'),
					'errors': obj.errors
				})

		# Сохраняем данные если ошибок нету
		if len(errors['validation_error'][context+'s']) == 0:
			response = {context+'s': []}
			for obj in valid_objects:
				response[context+'s'].append({'id': obj.initial_data.get(context+'_id')})
				obj.save()
			return Response(response, status=status.HTTP_201_CREATED)
		return Response(errors, status=status.HTTP_400_BAD_REQUEST)
