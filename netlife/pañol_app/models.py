from django.db import models
from sqlalchemy import null
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import logout
from django.dispatch import receiver


# Create your models here.
class Tecnico(models.Model):
    name=models.CharField(max_length=50)
    metros=models.IntegerField(blank=True)
    def __str__(self):
        return self.name + str(self.metros)

class EquiposRetirados(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.CharField(max_length=30)
    tecnico = models.CharField(max_length=120)
    equipo_instalado = models.CharField(max_length=120)
    mac_instalado = models.CharField(max_length=50)
    equipo_desinstalado= models.CharField(max_length=120)
    mac_desinstalado = models.CharField(max_length=50)
    numero_vt = models.CharField(max_length=50)
    numero_cliente = models.CharField(max_length=50)
    nombre_cliente =models.CharField(max_length=120)
    dni_cliente = models.CharField(max_length=50)
    direccion_cliente = models.CharField(max_length=120)
    localidad_cliente = models.CharField(max_length=50)
    partido_cliente = models.CharField(max_length=50)
    telefono_cliente = models.CharField(max_length=50)
    region_cliente =models.CharField(max_length=50)
    def __str__(self):
        return str(self.fecha)+str(self.tecnico)+str(self.equipo_instalado)+str(self.mac_instalado)+str(self.equipo_desinstalado)+str(self.mac_desinstalado)+str(self.numero_vt)+str(self.numero_cliente)+str(self.nombre_cliente)+str(self.dni_cliente)+str(self.direccion_cliente)+str(self.localidad_cliente)+str(self.partido_cliente)+str(self.telefono_cliente)+str(self.region_cliente)
    
    class Meta:
        unique_together = ['fecha', 'tecnico', 'equipo_instalado', 'mac_instalado', 'equipo_desinstalado', 'mac_desinstalado', 'numero_vt', 'numero_cliente', 'nombre_cliente', 'dni_cliente', 'direccion_cliente', 'localidad_cliente', 'partido_cliente', 'telefono_cliente', 'region_cliente']

class Equipo(models.Model):
    estado= models.CharField(max_length=60)
    nombre_equipo = models.CharField(max_length=120)
    seriado = models.CharField(max_length=30)
    fecha = models.CharField(max_length=30)
    def __str__(self):
        return  str(self.estado ) + str(self.nombre_equipo ) +str(self.seriado )  +str(self.fecha )


class Bobina_consumo(models.Model):
    consumo_bobina=models.CharField(max_length=30)
    tecnico=models.CharField(max_length=30)
    def __str__(self):
        return  str(self.consumo_bobina)+ str(self.tecnico)
class Bobina_hisotiral(models.Model):
    seriado_bobina=models.CharField(max_length=30)
    tecnico=models.CharField(max_length=30)
    def __str__(self):
        return  str(self.seriado_bobina)+str(self.tecnico)


class Descuento(models.Model):
    tecnico=models.CharField(max_length=30)
    equipo=models.CharField(max_length=30)
    mac=models.CharField(max_length=30, unique=True)
    vt=models.CharField(max_length=30)
    cliente=models.CharField(max_length=30)
    estado=models.CharField(max_length=30)
    def __str__(self):
        return  str(self.tecnico)+str(self.equipo)+str(self.mac)+str(self.vt)+str(self.cliente)+str(self.estado)
    

    