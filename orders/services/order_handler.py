import pytz
from datetime import timedelta, datetime

from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings

from orders.models import Order, OrderGroup, OrderDetail
from couriers.models import Courier
from core.utils import get_time_zone_client


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

	def __init__(self, courier_id, request):
		self.courier_id = courier_id
		self.request = request
		self.courier = self.get_courier()

	def __call__(self, status):
		try:
			order_group = OrderGroup.objects.get(courier=self.courier)
			orders = OrderHandlerTools.get_order_by_order_group(order_group)
			return Response(self.get_response(orders, order_group.assign_time, is_added=True), status=status)
		except OrderGroup.DoesNotExist:
			return Response(self.get_response(), status=status)

	def get_courier(self):
		"""Возвращаем курьера по его идентификатору"""
		return Courier.objects.get(courier_id=self.courier_id)

	def get_response(self, orders=None, assign_time=None, is_added=False):
		"""Формируем и возвращаем тело ответа"""
		if orders is None:
			orders = self.get_orders()

			if len(orders) == 0:
				return {'orders': []}

		if assign_time is None:
			assign_time = timezone.now()
			assign_time -= timedelta(microseconds=assign_time.microsecond)

		assign_time = assign_time.astimezone(get_time_zone_client(self.request))

		if not is_added:
			self.add_orders(orders, assign_time.strftime(settings.TIME_FORMAT))

		return {
			'orders': OrderHandlerTools.get_id_orders(orders),
			'assign_time': assign_time.strftime(settings.TIME_FORMAT)
		}

	def get_orders(self):
		"""Возвращаем заказы подходящие для конкретного курьера"""
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
		"""Формируем развоз для курьера из списка заказов"""
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
				region=order.region,
				courier_type=self.courier.courier_type
			)
			order_detail.save()
			order.status = 1
			order.save()


class OrderCompleteHandler:
	"""Обработчик завершения заказа"""

	def __init__(self, courier_id, order_id, complete_time, request):
		self.request = request
		self.complete_time = self.set_complete_time(complete_time)
		self.courier_id = int(courier_id)
		self.order_id = int(order_id)

	def __call__(self, status):
		self.order = Order.objects.get(order_id=self.order_id)
		if self.order.status == 1:
			self.save_completed_order()
		return Response(self.get_response(), status=status)

	def set_complete_time(self, complete_time):
		"""Преобразуем локальное время в серверное"""
		complete_time = datetime.strptime(complete_time, settings.TIME_FORMAT)
		complete_time = get_time_zone_client(self.request).localize(complete_time)
		complete_time = complete_time.astimezone(pytz.utc)
		return complete_time

	def get_response(self):
		"""Формируем и возвращаем тело ответа"""
		return {'order_id': self.order_id}

	def save_completed_order(self):
		"""Сохраняем завершение заказа"""
		self.order.status = 2
		order_detail = OrderDetail.objects.get(order=self.order)
		order_group = OrderGroup.objects.get(courier=order_detail.courier)
		order_detail.end_time = self.complete_time

		if order_detail.start_time is None:
			order_detail.start_time = order_group.assign_time

		self.order.save()
		order_detail.save()
		self.check_other_orders(order_group)

	def check_other_orders(self, order_group):
		"""
		Удаляем группу заказов(развоз), если заказов в нём не осталось,
		иначе устанавливаем время начала выполнения для оставшихся заказов.
		"""
		orders_detail = OrderDetail.objects.filter(order_group=order_group, order__status=1)

		if len(orders_detail) == 0:
			order_group.delete()
		else:
			for order_detail in orders_detail:
				order_detail.start_time = self.complete_time
				order_detail.save()


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
		"""Возвращаем курьера по его идентификатору"""
		return Courier.objects.get(courier_id=self.courier_id)

	def get_order_group(self):
		"""
		Возвращаем группу заказов(развоз) для конкретного
		курьера, None если такой группы нету.
		"""
		try:
			return OrderGroup.objects.get(courier=self.courier)
		except OrderGroup.DoesNotExist:
			return None

	def check_orders(self, order_group):
		"""
		Проверяем, может ли курьер выполнить выданные ему заказы,
		и убираем из развоза, если выполнение заказа невозможно.
		"""
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

		# Удаляем группу заказов(развоз), если заказов в нём не осталось
		if len(OrderDetail.objects.filter(order_group=order_group, order__status=1)) == 0:
			order_group.delete()

	@staticmethod
	def cancel_order(order_detail):
		"""
		Убираем заказ из развоза и делаем доступным
		для назначения этого заказа другим курьерам.
		"""
		order = order_detail.order
		order_detail.delete()
		order.status = 0
		order.save()
