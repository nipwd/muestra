from django.urls import path
from wolf_app import views
urlpatterns = [
    path('', views.get_binance_data, name='home'),
    path('prueba/', views.my_view, name='prueba'),
]
