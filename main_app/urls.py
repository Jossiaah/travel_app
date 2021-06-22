from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('trips/new', views.new_trip),
    path('trips/create', views.create_trip),
    path('trips/edit/<int:trip_id>', views.edit_trip),
    path('trips/update/<int:trip_id>', views.update_trip),
    path('trips/<int:trip_id>', views.trip_view),
    path('trips/delete/<int:trip_id>', views.delete_trip)
]
