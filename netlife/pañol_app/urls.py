from django.urls import path

from pañol_app.views import *
from django.contrib.auth.views import LogoutView
from pañol_app.views import handler404
urlpatterns = [
    path('',login_request, name='index'),
    path('tecnicos/',tecnicos, name='tecnicos'),
    path('verTecnico/<tecnico_name>', verTecnico, name="verTecnico"),
    path('stock/',stock, name='stock'),
    path('verStock/<tecnico_name>', verStock, name="verStock"),
    path('Ingresos/',Ingresos, name='Ingresos'),
    path('editar-equipo/', editar_equipo, name='editar_equipo'),
    path('mistock',mistock, name='mistock'),
    path('devolcuiones/',devoluciones, name='devolcuiones'),
    path('descuentos/', descuentos, name="descuentos"),
    path('login/', login_request, name='login'),
    path('logout/', LogoutView.as_view(template_name='templates/logout.html'),name='logout'),
]
handler404 = 'pañol_app.views.handler404'

