from django.db import models
from django.contrib.postgres.fields import ArrayField


class Courier(models.Model):
	"""Базовая модель курьера"""

	courier_id = models.IntegerField(
		verbose_name='Идентификатор курьера',
		unique=True,
		db_index=True
	)
	COURIER_TYPES = (
		('foot', 10),
		('bike', 15),
		('car', 50)
	)
	courier_type = models.CharField(
		verbose_name='Тип курьера',
		max_length=4,
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
