from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Courier
from .serializers import CourierCreateSerializer, CourierUpdateSerializer
from orders.services import order_handler
from core.views import CreateDataListMixin


class CourierCreateView(CreateDataListMixin, APIView):
	"""Добавление спаска курьеров"""

	def post(self, request, *args):
		return super().post(request, context='courier', serializer_class=CourierCreateSerializer)


class CourierDetailAndUpdateView(APIView):
	"""Частичное изменение курьера и подробная информация о нём"""

	def get(self, request, courier_id):
		pass

	def patch(self, request, courier_id):
		courier = CourierUpdateSerializer(
			get_object_or_404(Courier, courier_id=courier_id),
			data=request.data,
			partial=True
		)
		if courier.is_valid():
			courier.save()
			check = order_handler.PossibilityExecutionOrders(int(courier_id))
			check()
			return Response(courier.data, status=status.HTTP_200_OK)
		return Response(courier.errors, status=status.HTTP_400_BAD_REQUEST)
