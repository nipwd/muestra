from django.urls import path
from wolf_app import views

urlpatterns = [
    path('', views.home ,name='home'),

]
