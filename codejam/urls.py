from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('new/', views.reservation_create, name='reservation_create'),
    path('reservation/cancel/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),

]
