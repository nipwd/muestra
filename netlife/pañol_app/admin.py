from django.contrib import admin

from pañol_app.models import *

class EquipoAdmin(admin.ModelAdmin):
    search_fields = ('seriado',)
class TecnicoAdmin(admin.ModelAdmin):
    search_fields = ('name',)
class EquiposRetiradosAdmin(admin.ModelAdmin):
    search_fields = ('tecnico','mac_desinstalado','mac_instalado','numero_vt','numero_cliente','fecha')

# Register your models here.
admin.site.register(Tecnico, TecnicoAdmin)
admin.site.register(EquiposRetirados,EquiposRetiradosAdmin)
admin.site.register(Equipo, EquipoAdmin)

admin.site.register(Bobina_consumo)
admin.site.register(Bobina_hisotiral)
admin.site.register(Descuento)