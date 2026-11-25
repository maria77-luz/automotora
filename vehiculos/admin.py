
from django.contrib import admin
from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo', 'anio', 'precio', 'kilometraje', 'disponible')
    search_fields = ('marca', 'modelo')
    list_filter = ('anio', 'disponible')
