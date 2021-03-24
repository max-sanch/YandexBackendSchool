normal_create_couriers = {
	"data": [
		{
			"courier_id": 1,
			"courier_type": "foot",
			"regions": [1, 12, 22],
			"working_hours": ["11:35-14:05", "09:00-11:00"]
		},
		{
			"courier_id": 2,
			"courier_type": "bike",
			"regions": [22],
			"working_hours": ["09:00-18:00"]
		},
		{
			"courier_id": 3,
			"courier_type": "car",
			"regions": [12, 22, 23, 33],
			"working_hours": []
		},
		{
			"courier_id": 4,
			"courier_type": "bike",
			"regions": [23, 33],
			"working_hours": ["09:00-18:00"]
		},
		{
			"courier_id": 5,
			"courier_type": "foot",
			"regions": [1, 12],
			"working_hours": ["09:00-12:00", "13:00-15:00", "16:00-18:00"]
		}
	]
}

fail_create_couriers_data = {
	"data": [
		{
			"courier_id": 1,
			"courier_type": "foot",
			"regions": [1, 12, 22],
			"working_hours": ["11:35-14:99"]
		},
		{
			"courier_id": 2,
			"courier_type": "bus",
			"regions": [22]
		},
		{
			"courier_id": 3,
			"courier_type": "car",
			"regions": [12, 22, 23, 33],
			"working_hours": [],
			"courier_car": 1
		},
		{
			"courier_id": 4,
			"courier_type": "foot",
			"regions": [23, 33, "Первый"],
			"working_hours": ["09:00-18:00"]
		}
	]
}

fail_create_couriers_error = {
	"validation_error": {
		"couriers": [
			{
				"id": 1,
				"errors": {
					"working_hours": {
						"time_format": "Неверный формат времени. Нужен: HH:MM-HH:MM"
					}
				}
			},
			{
				"id": 2,
				"errors": {
					"courier_type": ["Значения bus нет среди допустимых вариантов."],
					"working_hours": ["Обязательное поле."]
				}
			},
			{
				"id": 3,
				"errors": {
					"fields": ["Получены неописанные поля: courier_car."]
				}
			},
			{
				"id": 4,
				"errors": {
					"regions": {
						"2": ["Введите правильное число."]
					}
				}
			}
		]
	}
}

normal_create_orders = {
	"data": [
		{
			"order_id": 1,
			"weight": 0.23,
			"region": 23,
			"delivery_hours": ["09:00-18:00"]
		},
		{
			"order_id": 2,
			"weight": 3.2,
			"region": 1,
			"delivery_hours": ["09:00-18:00"]
		},
		{
			"order_id": 3,
			"weight": 0.5,
			"region": 22,
			"delivery_hours": ["09:00-12:00", "16:00-21:30"]
		},
		{
			"order_id": 4,
			"weight": 15,
			"region": 1,
			"delivery_hours": ["09:00-10:00"]
		},
		{
			"order_id": 5,
			"weight": 8,
			"region": 33,
			"delivery_hours": ["09:00-12:00", "13:00-18:00"]
		},
		{
			"order_id": 6,
			"weight": 0.23,
			"region": 5,
			"delivery_hours": ["09:00-18:00"]
		},
		{
			"order_id": 7,
			"weight": 15,
			"region": 4,
			"delivery_hours": ["09:00-18:00"]
		},
		{
			"order_id": 8,
			"weight": 0.01,
			"region": 1,
			"delivery_hours": ["16:00-21:30"]
		},
		{
			"order_id": 9,
			"weight": 1,
			"region": 3,
			"delivery_hours": ["09:00-10:00"]
		},
		{
			"order_id": 10,
			"weight": 8,
			"region": 2,
			"delivery_hours": ["09:00-12:00", "13:00-18:00"]
		}
	]
}

fail_create_orders_data = {
	"data": [
		{
			"order_id": 1,
			"weight": 0.23,
			"region": 12,
			"delivery_hours": ["09:00-18:99"]
		},
		{
			"order_id": 2,
			"weight": 15,
			"delivery_hours": ["09:00-18:00"]
		},
		{
			"order_id": 3,
			"weight": 0.01,
			"region": 22,
			"delivery_hours": ["09:00-12:00", "16:00-21:30"],
			"order": 3
		},
		{
			"order_id": 4,
			"weight": 51,
			"region": 23,
			"delivery_hours": ["09:00-10:00"]
		}
	]
}

fail_create_orders_error = {
	'validation_error': {
		'orders': [
			{
				'id': 1,
				'errors': {
					'delivery_hours': {
						'time_format': 'Неверный формат времени. Нужен: HH:MM-HH:MM'
					}
				}
			},
			{
				'id': 2,
				'errors': {
					'region': ['Обязательное поле.']
				}
			},
			{
				'id': 3,
				'errors': {
					'fields': ['Получены неописанные поля: order.']
				}
			},
			{
				'id': 4,
				'errors': {
					'weight': ['Убедитесь, что это значение меньше либо равно 50.']
				}
			}
		]
	}
}
