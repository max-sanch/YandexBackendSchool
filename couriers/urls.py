from django.urls import path
from couriers import views

urlpatterns = [
	path('/<int:courier_id>', views.CourierDetailAndUpdateView.as_view(), name='one_courier'),
	path('', views.CourierCreateView.as_view(), name='create_couriers'),
]
