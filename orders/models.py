from django.db import models
from django.contrib.postgres.fields import ArrayField

from couriers.models import Courier


class Order(models.Model):
	"""Базовая модель заказа"""

	order_id = models.IntegerField(
		verbose_name='Идентификатор заказа',
		unique=True,
		db_index=True
	)
	weight = models.FloatField(verbose_name='Вес заказа')
	region = models.IntegerField(verbose_name='Район доставки заказа')
	delivery_hours = ArrayField(
		models.CharField(max_length=11),
		size=None,
		verbose_name='Промежутки приёма заказов'
	)
	STATUSES = (
		(0, 'Новый'),
		(1, 'В работе'),
		(2, 'Завершённый')
	)
	status = models.IntegerField(
		verbose_name='Вес заказа',
		choices=STATUSES,
		default=0
	)
	objects = models.Manager()


class OrderGroup(models.Model):
	"""Группа заказов выполняющаяся одним курьером"""

	courier = models.OneToOneField(
		'couriers.Courier',
		on_delete=models.CASCADE,
		verbose_name='Курьер выполняющий группу заказов'
	)
	assign_time = models.DateTimeField(
		verbose_name='Время выбора заказов',
		auto_now_add=True
	)
	objects = models.Manager()


class OrderDetail(models.Model):
	"""Информация о взятых в работу и завершённых заказах"""

	order = models.OneToOneField(
		Order,
		on_delete=models.CASCADE,
		verbose_name='Заказ'
	)
	courier = models.ForeignKey(
		'couriers.Courier',
		on_delete=models.CASCADE,
		verbose_name='Курьер выполняющий заказ'
	)
	order_group = models.ForeignKey(
		OrderGroup,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		verbose_name='Группа заказа'
	)
	region = models.IntegerField(verbose_name='Район доставки заказа')
	courier_type = models.CharField(
		verbose_name='Тип курьера исполняющего заказ',
		max_length=4,
		choices=Courier.COURIER_TYPES
	)
	start_time = models.DateTimeField(
		verbose_name='Начало выполнения заказа',
		null=True,
		default=None
	)
	end_time = models.DateTimeField(
		verbose_name='Окончание выполнения заказа',
		null=True,
		default=None
	)
	objects = models.Manager()
