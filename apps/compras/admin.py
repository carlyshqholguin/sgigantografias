from django.contrib import admin
from .models import Compra, Insumo, Proveedor, DetalleCompra
from django.db.models import Sum

class DetalleCompraInline(admin.TabularInline):  # Puedes usar StackedInline si prefieres un diseño diferente
    model = DetalleCompra
    extra = 1  # Número de formularios en blanco a mostrar para la relación DetalleCompra en la página de edición de Compra

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id_compra', 'proveedor', 'inventario', 'total_compra', 'factura', 'created_at', 'updated_at')
    list_filter = ('proveedor', 'inventario', 'factura')
    search_fields = ['id_compra', 'proveedor__nombre']  # Puedes personalizar esto según tus necesidades
    ordering = ('-created_at',)
    list_per_page = 10
    inlines = [DetalleCompraInline]



@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('id_insumo', 'proveedor', 'nombre', 'categoria', 'precio', 'created_at', 'updated_at')
    list_filter = ('categoria', 'proveedor')
    search_fields = ['id_insumo', 'nombre', 'proveedor__nombre']
    readonly_fields = ['id_insumo', 'created_at', 'updated_at']
    ordering = ('-created_at',)
    list_per_page = 10


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id_proveedor', 'nombre', 'direccion', 'correo_electronico', 'celular', 'nit', 'razon_social', 'created_at', 'updated_at')
    search_fields = ['id_proveedor', 'nombre', 'nit']
    readonly_fields = ['id_proveedor', 'created_at', 'updated_at']
    ordering = ('-created_at',)
    list_per_page = 10

