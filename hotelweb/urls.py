from django.urls import path
from . import views
from login.views import logout_view
from .views import update_booking

app_name = 'hotelweb'

urlpatterns = [
    # URLs pour les réservations
    path('booking/', views.booking_page, name='booking'),
    path('booking/list/', views.booking_list, name='booking_list'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('booking/update/', update_booking, name='update_booking'),
    path('booking/check-availability/', views.check_room_availability, name='check_room_availability'),
    
    # URLs pour les chambres
    path('room/', views.room_page, name='room'),
    path('room/list/', views.room_list, name='room_list'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('get-available-rooms/', views.get_available_rooms, name='get_available_rooms'),

    # URL pour About Us
    path('about-us/', views.about_us, name='about_us'),

    # URL pour Admin Dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/booking/', views.admin_booking, name='admin_booking'),
    path('admin/about-us/', views.admin_about_us, name='admin_about_us'),
    path('admin/room/', views.admin_room, name='admin_room'),
    path('admin/payment/', views.admin_payment, name='admin_payment'),

    # URL pour Logout
    path('logout/', logout_view, name='logout'),

    # URL pour Payement
    path('payement/', views.payement, name='payement'),
    path('process-payment/', views.process_payment, name='process_payment'),
]