from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('trips/create/', views.create_trip, name='create_trip'),
    path('trips/search/', views.search_trips, name='search_trips'),
    path('trips/my/', views.my_trips, name='my_trips'),
    path('trips/<int:trip_id>/edit/', views.edit_trip, name='edit_trip'),
    path('trips/<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
    path('requests/create/', views.create_request, name='create_request'),
] 