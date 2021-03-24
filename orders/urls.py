from django.urls import path
from orders import views

urlpatterns = [
	path('/assign', views.OrderAssignView.as_view(), name='assign_order'),
	path('/complete', views.OrderCompleteView.as_view(), name='complete_order'),
	path('', views.OrderCreateView.as_view(), name='create_orders'),
]
