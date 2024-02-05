from django.db import models
import uuid
import shortuuid
from apps.compras.models import Insumo

def conver_encode():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return s


class Sucursal(models.Model):
    id_sucursal = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    nombre = models.CharField(max_length=155, blank=False, null=False,verbose_name="Nombre")
    direccion = models.CharField(max_length=255, blank=False, null=False,verbose_name="Dirección")
    latitud = models.CharField(max_length=55, blank=True, null=True,verbose_name="Latitud")
    longitud = models.CharField(max_length=55, blank=True, null=True,verbose_name="Longitud")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta():
        verbose_name="Sucursal"
        verbose_name_plural="Sucursales"
        db_table="sucursal"

class Inventario(models.Model):
    id_inventario = models.CharField(primary_key=True, max_length=100, unique=True, default=conver_encode, editable=False)
    sucursal = models.OneToOneField(Sucursal, blank=False, null=False, related_name="inventario", on_delete=models.CASCADE, verbose_name="Sucursal")
    nombre = models.CharField(max_length=155, blank=False, null=False, verbose_name="Nombre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"

class StockInsumo(models.Model):
    id_stock_insumo = models.CharField(primary_key=True, max_length=100, unique=True, default=conver_encode, editable=False)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name="stocks", verbose_name="Inventario")
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, verbose_name="Insumo")
    cantidad = models.IntegerField(default=0, blank=False, null=False, verbose_name="Cantidad en stock")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.insumo.nombre} en {self.inventario.nombre}: {self.cantidad}"

    class Meta:
        verbose_name = "Stock de Insumo"
        verbose_name_plural = "Stocks de Insumos"
        db_table = "stock_insumo"

class Servicio(models.Model):
    id_servicio = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    nombre = models.CharField(max_length=155, blank=False, null=False,verbose_name="Nombre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta():
        verbose_name="Servicio"
        verbose_name_plural="Servicios"
        db_table="servicio"


class Caracteristica(models.Model):
    id_caracteristica = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    servicio=models.ForeignKey(Servicio,blank=False,null=False,related_name="caracteristicas",on_delete=models.CASCADE,verbose_name="Servicio")
    detalle = models.TextField(max_length=500, blank=True, null=True,verbose_name="Detalle")
    precio=models.FloatField(default=0,verbose_name="Precio")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_servicio
    
    class Meta():
        verbose_name="Característica"
        verbose_name_plural="Características"
        db_table="caracteristica"