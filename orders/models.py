from django.db import models
from django.contrib.postgres.fields import ArrayField

from couriers.models import Courier


class Order(models.Model):
	"""Базовая модель заказа"""
	order_id = models.IntegerField(
		verbose_name='Уникальный идентификатор заказа',
		unique=True,
		db_index=True
	)
	weight = models.FloatField(verbose_name='Вес заказа')
	region = models.IntegerField(verbose_name='Район доставки заказа')
	delivery_hours = ArrayField(
		models.CharField(max_length=11),
		size=None,
		verbose_name='График работы курьера'
	)
	STATUSES = (
		(0, 'Новый'),
		(1, 'В работе'),
		(2, 'Завершённый')
	)
	status = models.IntegerField(
		verbose_name='Вес заказа',
		choices=STATUSES
	)


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


class OrderDetail(models.Model):
	"""Информация о взятых в работу и завершённых заказов"""
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
	courier_type = models.IntegerField(
		verbose_name='Тип курьера исполняющего заказ',
		choices=Courier.COURIER_TYPES
	)
	start_time = models.DateTimeField(
		verbose_name='Начало выполнения заказа',
		null=True,
		blank=True
	)
	end_time = models.DateTimeField(
		verbose_name='Окончание выполнения заказа',
		null=True,
		blank=True
	)
