from datetime import timedelta

from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings

from orders.models import Order, OrderGroup, OrderDetail
from couriers.models import Courier


class OrderHandlerTools:
	"""Набор функций для работы с заказами"""

	@classmethod
	def get_minute_list(cls, period_list):
		"""
		Возвращаем список минут в которые работает
		курьер или принимается заказ.
		"""
		result = set()
		for period in period_list:
			result |= set(cls.get_period(period))
		return result

	@classmethod
	def get_period(cls, period):
		"""
		Преобразуем промежуток времени из вида 'HH:MM-HH:MM'
		в промежуток минут полученый по формуле HH*60+MM.
		"""
		start, end = map(lambda x: int(x[:2])*60 + int(x[3:]), period.split('-'))
		return range(start, end)

	@classmethod
	def get_id_orders(cls, orders):
		"""
		Возвращаем список словарей вида {"id": order_id},
		где order_id получаем из списка заказов.
		"""
		return [{'id': x.order_id} for x in orders]

	@classmethod
	def get_order_by_order_group(cls, order_group, status=1):
		"""Возвращаем список заказов из конкретной группы"""
		return [x.order for x in OrderDetail.objects.filter(order_group=order_group, order__status=status)]


class OrderAssignHandler:
	"""Обработчик подбора заказов для курьера"""

	def __init__(self, courier_id):
		self.courier_id = courier_id
		self.courier = self.get_courier()

	def __call__(self, status):
		try:
			order_group = OrderGroup.objects.get(courier=self.courier)
			orders = OrderHandlerTools.get_order_by_order_group(order_group)
			return Response(self.get_response(orders, order_group.assign_time, is_added=True), status=status)
		except OrderGroup.DoesNotExist:
			return Response(self.get_response(), status=status)

	def get_courier(self):
		return Courier.objects.get(courier_id=self.courier_id)

	def get_response(self, orders=None, assign_time=None, is_added=False):
		if orders is None:
			orders = self.get_orders()

			if len(orders) == 0:
				return {'orders': []}

		if assign_time is None:
			assign_time = timezone.now().strftime(settings.TIME_FORMAT)
		else:
			assign_time -= timedelta(microseconds=assign_time.microsecond)
			assign_time.strftime(settings.TIME_FORMAT)

		if not is_added:
			self.add_orders(orders, assign_time)
		return {'orders': OrderHandlerTools.get_id_orders(orders), 'assign_time': assign_time}

	def get_orders(self):
		max_weight = dict(Courier.COURIER_TYPES).get(self.courier.courier_type)
		orders = Order.objects.filter(
			status=0,
			weight__lte=max_weight,
			region__in=self.courier.regions
		).order_by('weight')
		courier_minutes = OrderHandlerTools.get_minute_list(self.courier.working_hours)
		result = []
		weight = 0

		for order in orders:
			if len(courier_minutes & OrderHandlerTools.get_minute_list(order.delivery_hours)) != 0:
				if weight + order.weight <= max_weight:
					result.append(order)
					weight += order.weight
				else:
					break
		return result

	def add_orders(self, orders, assign_time):
		order_group = OrderGroup(
			courier=self.courier,
			assign_time=assign_time,
		)
		order_group.save()
		for order in orders:
			order_detail = OrderDetail(
				order=order,
				courier=self.courier,
				order_group=order_group,
				courier_type=self.courier.courier_type
			)
			order_detail.save()
			order.status = 1
			order.save()


class PossibilityExecutionOrders:
	"""Проверка возможности выполнения заказов курьером"""

	def __init__(self, courier_id):
		self.courier_id = courier_id
		self.courier = self.get_courier()

	def __call__(self):
		order_group = self.get_order_group()
		if order_group is not None:
			self.check_orders(order_group)

	def get_courier(self):
		return Courier.objects.get(courier_id=self.courier_id)

	def get_order_group(self):
		try:
			return OrderGroup.objects.get(courier=self.courier)
		except OrderGroup.DoesNotExist:
			return None

	def check_orders(self, order_group):
		orders_detail = OrderDetail.objects.filter(order_group=order_group, order__status=1).order_by('order__weight')
		max_weight = dict(Courier.COURIER_TYPES).get(self.courier.courier_type)
		courier_minutes = OrderHandlerTools.get_minute_list(self.courier.working_hours)
		check_weight = False
		weight = 0

		if orders_detail[0].courier_type != self.courier.courier_type:
			check_weight = True

		for order_detail in orders_detail:
			if check_weight:
				order_detail.courier_type = self.courier.courier_type
				order_detail.save()
				weight += order_detail.order.weight

			if weight > max_weight or order_detail.order.region not in self.courier.regions or \
				len(courier_minutes & OrderHandlerTools.get_minute_list(order_detail.order.delivery_hours)) == 0:
				self.cancel_order(order_detail)

		if len(OrderDetail.objects.filter(order_group=order_group, order__status=1)) == 0:
			order_group.delete()

	@staticmethod
	def cancel_order(order_detail):
		order = order_detail.order
		order_detail.delete()
		order.status = 0
		order.save()
