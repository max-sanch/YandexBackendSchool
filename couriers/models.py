from django.db import models
from django.contrib.postgres.fields import ArrayField


class Courier(models.Model):
	"""Базовая модель курьера"""
	courier_id = models.IntegerField(
		verbose_name='Уникальный идентификатор курьера',
		unique=True,
		db_index=True
	)
	COURIER_TYPES = (
		(0, 'foot'),
		(1, 'bike'),
		(2, 'car')
	)
	courier_type = models.IntegerField(
		verbose_name='Тип курьера',
		choices=COURIER_TYPES
	)
	regions = ArrayField(
		models.IntegerField(),
		size=None,
		verbose_name='Список идентификаторов районов'
	)
	working_hours = ArrayField(
		models.CharField(max_length=11),
		size=None,
		verbose_name='График работы курьера'
	)
	objects = models.Manager()
