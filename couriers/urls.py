from django.urls import path
from couriers import views

urlpatterns = [
	path('<int:courier_id>/', views.CourierView.as_view()),
	path('', views.CourierView.as_view()),
]
