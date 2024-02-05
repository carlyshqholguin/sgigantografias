from django.contrib import admin
from .models import Sucursal,Caracteristica,Servicio,Inventario,StockInsumo

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id_sucursal', 'nombre', 'direccion', 'latitud', 'longitud', 'created_at', 'updated_at')
    search_fields = ['id_sucursal', 'nombre', 'direccion']
    readonly_fields = ['id_sucursal', 'created_at', 'updated_at']
    ordering = ('-created_at',)
    list_per_page = 10


class CaracteristicaInline(admin.TabularInline):
    model = Caracteristica
    extra = 1

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id_servicio', 'nombre', 'created_at', 'updated_at')
    search_fields = ['id_servicio', 'nombre']
    readonly_fields = ['id_servicio', 'created_at', 'updated_at']
    ordering = ('-created_at',)
    list_per_page = 10
    inlines = [CaracteristicaInline]

class StockInsumoInline(admin.TabularInline):  # Puedes usar StackedInline si prefieres un diseño diferente
    model = StockInsumo
    extra = 1 

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('id_inventario', 'sucursal', 'nombre', 'created_at', 'updated_at')
    list_filter = ('sucursal',)
    search_fields = ['id_inventario', 'nombre', 'sucursal__nombre']
    ordering = ('-created_at',)
    list_per_page = 10
    inlines = [StockInsumoInline]

