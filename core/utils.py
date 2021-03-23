import pytz

from geoip2 import errors
from django.contrib.gis.geoip2 import GeoIP2


def get_client_ip(request):
	"""Возвращаем IP клиента"""
	return request.META.get('HTTP_X_REAL_IP', '0.0.0.0')


def get_time_zone_client(request):
	"""Возвращаем часовой пояс клиента"""
	user_time_zone = request.session.get('user_time_zone', None)
	geoip = GeoIP2()
	try:
		if user_time_zone is None:
			city = geoip.city(get_client_ip(request))
			user_time_zone = city.get('time_zone')
		return pytz.timezone(user_time_zone)
	except errors.AddressNotFoundError:
		return pytz.timezone('Europe/Moscow')
