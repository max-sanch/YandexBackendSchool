from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import order_handler
from .serializers import OrderCreateSerializer, OrderAssignSerializer
from core.views import CreateDataListMixin


class OrderCreateView(CreateDataListMixin, APIView):
	"""Добавление спаска заказов"""

	def post(self, request, *args):
		return super().post(request, context='order', serializer_class=OrderCreateSerializer)


class OrderAssignView(APIView):
	"""Формирование группы заказов для курьера"""

	def post(self, request):
		courier_id = OrderAssignSerializer(data=request.data)
		if courier_id.is_valid():
			response = order_handler.OrderAssignHandler(courier_id.data.get('courier_id'))
			return response(status=status.HTTP_200_OK)
		return Response(courier_id.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCompleteView(APIView):
	"""Завершение заказа"""

	def post(self, request):
		pass
