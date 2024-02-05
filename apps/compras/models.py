from django.db import models
import uuid
import shortuuid
from django.db.models.signals import post_save
from django.dispatch import receiver



def conver_encode():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return s


class Compra(models.Model):
    id_compra = models.CharField(primary_key=True, max_length=100, unique=True, default=conver_encode, editable=False)
    proveedor = models.ForeignKey('Proveedor', blank=False, null=False, related_name="compras", on_delete=models.CASCADE, verbose_name="Proveedor")
    inventario = models.ForeignKey('empresa.Inventario', blank=False, null=False, related_name="compras", on_delete=models.CASCADE, verbose_name="Inventario")
    total_compra = models.FloatField(default=0, blank=False, null=False, verbose_name="Total de la compra", editable=False)
    factura = models.BooleanField(default=False, verbose_name="Facturado")
    impuesto_iva = models.IntegerField(default=13, blank=False, null=False, verbose_name="IMPUESTO IVA %", editable=False)
    impuesto_it = models.IntegerField(default=3, blank=False, null=False, verbose_name="IMPUESTO IT %", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_compra

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        db_table = "compra"


class DetalleCompra(models.Model):
    id_detalle_compra = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name='detalles',verbose_name="Compra")
    insumo = models.ForeignKey('Insumo', on_delete=models.CASCADE,verbose_name="Insumo")
    cantidad = models.PositiveIntegerField(default=0,verbose_name="Cantidad",blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.insumo.nombre} ({self.cantidad})"
    
    class Meta():
        verbose_name="Detalle de la Compra"
        verbose_name_plural="Detalles de las Compras"
        db_table="detalle_compra"


@receiver(post_save, sender=DetalleCompra)
def handle_detalle_compra_post_save(sender, instance, **kwargs):
    from apps.ventas.models import Factura, Recibo
    from apps.empresa.models import StockInsumo
    
    compra = instance.compra

    # Calcula el total de la compra
    suma_precios = sum(detalle.insumo.precio * detalle.cantidad for detalle in compra.detalles.all())
    compra.total_compra = suma_precios

    # Aplica impuestos si la compra está facturada
    if compra.factura:
        impuesto_total = compra.impuesto_iva + compra.impuesto_it
        compra.total_compra += (compra.total_compra * impuesto_total) / 100

        # Verifica si ya existe una factura para esta compra
        factura_existente = Factura.objects.filter(tipo='Compra', detalle__icontains=f'Detalle de la compra {compra.id_compra}').first()

        if factura_existente:
            # Actualiza el total de la factura existente
            factura_existente.total = compra.total_compra
            factura_existente.save()
        else:
            # Crea la factura
            factura = Factura(
                nit=compra.proveedor.nit,
                razon_social=compra.proveedor.razon_social,
                tipo='Compra',
                detalle=f'Detalle de la compra {compra.id_compra}. Insumos: {", ".join(detalle.insumo.nombre for detalle in compra.detalles.all())}',
                total=compra.total_compra
            )
            factura.save()
    else:
        # Verifica si ya existe un recibo para esta compra
        recibo_existente = Recibo.objects.filter(tipo='Compra', detalle__icontains=f'Detalle del recibo de la compra {compra.id_compra}').first()

        if recibo_existente:
            # Actualiza el total del recibo existente
            recibo_existente.total = compra.total_compra
            recibo_existente.save()
        else:
            # Crea el recibo
            recibo = Recibo(
                tipo='Compra',
                detalle=f'Detalle del recibo de la compra {compra.id_compra}. Insumos: {", ".join(detalle.insumo.nombre for detalle in compra.detalles.all())}',
                total=compra.total_compra
            )
            recibo.save()

    # Actualiza el stock de insumos en el inventario
    for detalle in compra.detalles.all():
        stock, created = StockInsumo.objects.get_or_create(
            inventario=compra.inventario,
            insumo=detalle.insumo
        )

        stock.cantidad += detalle.cantidad
        stock.save()

    compra.save()


CHOICES_CATEGORIA=[
    ('Materiales de Impresion','Materiales de Impresion'),
    ('Herramientas y Equipos','Herramientas y Equipos'),
    ('Partes y Accesorios','Partes y Accesorios'),
    ('Embalaje','Embalaje'),
]

class Insumo(models.Model):
    id_insumo = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    proveedor=models.ForeignKey('Proveedor',blank=False,null=False,related_name="insumos",on_delete=models.CASCADE,verbose_name="Proveedor")
    nombre = models.CharField(max_length=155, blank=False, null=False,verbose_name="Nombre")
    detalle = models.TextField(max_length=500, blank=True, null=True,verbose_name="Detalle")
    categoria = models.CharField(max_length = 125,verbose_name="Categoria",choices=CHOICES_CATEGORIA,blank=False,null=False)
    precio=models.FloatField(default=0,verbose_name="Precio")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta():
        verbose_name="Insumo"
        verbose_name_plural="Insumos"
        db_table="insumo"


class Proveedor(models.Model):
    id_proveedor = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    nombre = models.CharField(max_length=155, blank=False, null=False,verbose_name="Nombre")
    direccion = models.CharField(max_length=255, blank=False, null=False,verbose_name="Dirección")
    correo_electronico = models.EmailField(max_length=255, blank=False, null=False,verbose_name="Correo Electrónico")
    celular = models.CharField(max_length=255, blank=True, null=True,verbose_name="Número de celular")
    nit = models.CharField(max_length=55, blank=True, null=True,verbose_name="NIT")
    razon_social = models.CharField(max_length=255, blank=True, null=True,verbose_name="Razón social")
    latitud = models.CharField(max_length=55, blank=True, null=True,verbose_name="Latitud")
    longitud = models.CharField(max_length=55, blank=True, null=True,verbose_name="Longitud")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta():
        verbose_name="Proveedor"
        verbose_name_plural="Proveedores"
        db_table="proveedor"
