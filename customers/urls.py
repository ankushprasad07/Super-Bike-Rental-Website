from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_customer, name='customer_register'),
    path('login/', views.login_customer, name='customer_login'),
    path('logout/', views.logout_customer, name='customer_logout'),

    path('', views.bike_list, name='bike_list'),  # home page
    path('bike/<int:bike_id>/', views.bike_detail, name='bike_detail'),
    path('book-bike/<int:bike_id>/', views.booking_form, name='booking_form'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
]
