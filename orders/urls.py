from django.urls import path
from orders import views

urlpatterns = [
	path('assign/', views.OrderAssignView.as_view()),
	path('complete/', views.OrderCompleteView.as_view()),
	path('', views.OrderCreateView.as_view()),
]
