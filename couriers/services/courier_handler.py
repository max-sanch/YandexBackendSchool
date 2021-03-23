from orders.models import OrderDetail


class CourierRatingAndEarnings:
	"""Расчёт рейтинга и заработка курьера"""

	def __init__(self, courier):
		self.courier = courier
		self.orders_detail = self.get_order_detail()
		self.earnings = self.get_earnings()
		self.rating = self.get_rating()

	def get_order_detail(self):
		"""Возвращаем список заказов выполненных конкретным курьером"""
		return OrderDetail.objects.filter(courier=self.courier, order__status=2)

	def get_earnings(self):
		"""
		Возвращаем заработок курьера за выполненные заказы
		с учетом коэффициента зависящего от типа курьера.
		"""
		coefficient = {'foot': 2, 'bike': 5, 'car': 9}
		earnings = 0

		for order_detail in self.orders_detail:
			earnings += 500 * coefficient.get(order_detail.courier_type)
		return earnings

	def get_rating(self):
		"""
		Возвращаем рейтинг курьера рассчитанный по формуле:
		(60*60 - min(t, 60*60))/(60*60) * 5, где t - минимальное
		из средних времен доставки по районам.
		"""
		if len(self.orders_detail) == 0:
			return None
		return round((3600 - min(min(self.get_average_regions_time()), 3600))/3600 * 5, 2)

	def get_average_regions_time(self):
		"""Возвращаем список средних времен доставки по районам"""
		regions = dict()

		for order_detail in self.orders_detail:
			difference = order_detail.end_time - order_detail.start_time
			if regions.get(str(order_detail.region)) is None:
				regions.update({str(order_detail.region): [difference.seconds]})
			else:
				regions[str(order_detail.region)].append(difference.seconds)
		return [sum(x)/len(x) for x in regions.values()]
