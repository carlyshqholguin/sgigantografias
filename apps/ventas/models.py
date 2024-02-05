from django.db import models
import uuid
import shortuuid
from apps.compras.models import Insumo
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models.signals import post_save
import google.generativeai as palm
from dotenv import load_dotenv
from translate import Translator
import os
from apps.empresa.models import Servicio
import requests
from easygoogletranslate import EasyGoogleTranslate
from datetime import datetime, timedelta
import pywhatkit 
from django.db.models.signals import pre_save


def conver_encode():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return s


class Cliente(models.Model):
    id_cliente = models.CharField(
        primary_key=True,
        max_length=100,
        unique=True,
        default=conver_encode,
        editable=False,
    )
    nombre = models.CharField(
        max_length=155, blank=False, null=False, verbose_name="Nombres"
    )
    apellidos = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Apellidos"
    )
    direccion = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Direccion"
    )
    correo_electronico = models.EmailField(
        max_length=255, blank=False, null=False, verbose_name="Correo Electrónico"
    )
    celular = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Número de celular"
    )
    nit = models.CharField(max_length=55, blank=True, null=True, verbose_name="NIT")
    razon_social = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Razón social"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre + " " + self.apellidos

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = "cliente"

CHOICES_FASE = [
    ("Pendiente", "Pendiente"),
    ("Rayado y corte", "Rayado y corte"),
    ("Impresion", "Impresion"),
    ("Acabado final", "Acabado final"),
    ("Entregado", "Entregado"),
]

class Fase(models.Model):
    id_fase = models.CharField(
        primary_key=True,
        max_length=100,
        unique=True,
        default=conver_encode,
        editable=False,
    )
    cliente = models.ForeignKey(
        Cliente,
        blank=True,
        null=True,
        related_name="fases",
        on_delete=models.CASCADE,
        verbose_name="Cliente",
    )
    fase = models.CharField(
        max_length=125,
        verbose_name="Fase",
        choices=CHOICES_FASE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Fase"
        verbose_name_plural = "Fases"
        db_table = "fase"



class Cotizacion(models.Model):
    id_cotizacion = models.CharField(
        primary_key=True,
        max_length=100,
        unique=True,
        default=conver_encode,
        editable=False,
    )
    cliente = models.ForeignKey(
        Cliente,
        blank=True,
        null=True,
        related_name="cotizaciones",
        on_delete=models.CASCADE,
        verbose_name="Cliente",
    )
    insumos = models.ManyToManyField(Insumo, verbose_name="Insumos")
    total = models.FloatField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Total de la cotizacion",
        editable=False,
    )
    impuesto = models.IntegerField(
        default=0, blank=False, null=False, verbose_name="Impuesto (%)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_cotizacion

    class Meta:
        verbose_name = "Cotizacion"
        verbose_name_plural = "Cotizaciones"
        db_table = "cotizacion"


@receiver(m2m_changed, sender=Cotizacion.insumos.through)
def update_total_on_insumos_change(sender, instance, **kwargs):
    precios_insumos = [insumo.precio for insumo in instance.insumos.all()]
    suma_precios = sum(precios_insumos)

    if instance.impuesto > 0:
        impuesto_calculado = (suma_precios * instance.impuesto) / 100
        instance.total = suma_precios + impuesto_calculado
    else:
        instance.total = suma_precios

    instance.save()


CHOICES_TIPO = [
    ("Servicio", "Servicio"),
    ("Compra", "Compra"),
]


class Factura(models.Model):
    id_factura = models.CharField(
        primary_key=True,
        max_length=100,
        unique=True,
        default=conver_encode,
        editable=False,
    )
    nit = models.CharField(max_length=55, blank=True, null=True, verbose_name="NIT")
    razon_social = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Razón social"
    )
    tipo = models.CharField(
        max_length=125,
        verbose_name="Tipo",
        choices=CHOICES_TIPO,
        blank=False,
        null=False,
    )
    detalle = models.TextField(
        max_length=800, blank=True, null=True, verbose_name="Detalle"
    )
    total = models.FloatField(blank=False, null=False, verbose_name="Total")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_compra

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        db_table = "factura"


CHOICES_TIPO = [
    ("Servicio", "Servicio"),
    ("Compra", "Compra"),
]


class Recibo(models.Model):
    id_recibo = models.CharField(
        primary_key=True,
        max_length=100,
        unique=True,
        default=conver_encode,
        editable=False,
    )
    tipo = models.CharField(
        max_length=125,
        verbose_name="Tipo",
        choices=CHOICES_TIPO,
        blank=False,
        null=False,
    )
    detalle = models.TextField(
        max_length=800, blank=True, null=True, verbose_name="Detalle"
    )
    total = models.FloatField(blank=False, null=False, verbose_name="Total")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_recibo

    class Meta:
        verbose_name = "Recibo"
        verbose_name_plural = "Recibos"
        db_table = "recibo"


CHOICES_TIPO = [
    ("Servicio", "Servicio"),
]


class Venta(models.Model):
    id_venta = models.CharField(
        primary_key=True,
        max_length=100,
        unique=True,
        default=conver_encode,
        editable=False,
    )
    cliente = models.ForeignKey(
        Cliente,
        blank=False,
        null=False,
        related_name="ventas",
        on_delete=models.CASCADE,
        verbose_name="Cliente",
    )
    tipo = models.CharField(
        max_length=125,
        verbose_name="Tipo",
        choices=CHOICES_TIPO,
        blank=False,
        null=False,
    )
    inventario = models.ForeignKey(
        "empresa.Inventario",
        blank=False,
        null=False,
        related_name="ventas",
        on_delete=models.CASCADE,
        verbose_name="Inventario",
    )
    costo_impresion = models.FloatField(
        default=0, blank=False, null=False, verbose_name="Costo de Impresion"
    )
    costo_trabajo = models.FloatField(
        default=0, blank=False, null=False, verbose_name="Costo de Trabajo"
    )
    total_venta = models.FloatField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Total de la venta",
        editable=False,
    )
    factura = models.BooleanField(default=False, verbose_name="Facturado")
    insumos = models.ManyToManyField(
        Insumo, verbose_name="Insumos", related_name="detalles_ventas"
    )
    impuesto_iva = models.IntegerField(
        default=13,
        blank=False,
        null=False,
        verbose_name="IMPUESTO IVA %",
        editable=False,
    )
    impuesto_it = models.IntegerField(
        default=3, blank=False, null=False, verbose_name="IMPUESTO IT %", editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_venta
    



    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = "venta"


@receiver(m2m_changed, sender=Venta.insumos.through)
def handle_insumos_changed(sender, instance, action, **kwargs):
    if action == "post_add" or action == "post_remove":
        update_stock_and_totals(instance)

tiempo_actual = datetime.now()
tiempo_margen = tiempo_actual + timedelta(minutes=1)

def update_stock_and_totals(venta):
    from apps.empresa.models import StockInsumo

    # Calcula el total de la venta
    suma_precios = sum(insumo.precio for insumo in venta.insumos.all())
    venta.total_venta = suma_precios + venta.costo_impresion + venta.costo_trabajo

    # Aplica impuestos si la venta está facturada
    if venta.factura:
        impuesto_total = venta.impuesto_iva + venta.impuesto_it
        venta.total_venta += (venta.total_venta * impuesto_total) / 100

        # Verifica si ya existe una factura para esta venta
        factura_existente = Factura.objects.filter(
            tipo="Servicio", detalle__icontains=f"Detalle del servicio {venta.id_venta}"
        ).first()

        if factura_existente:
            # Actualiza el total de la factura existente
            factura_existente.total = venta.total_venta
            factura_existente.save()
        else:
            # Crea la factura
            factura = Recibo(
                nit=venta.cliente.nit,
                razon_social=venta.cliente.razon_social,
                tipo="Servicio",
                detalle=f'Detalle del servicio {venta.id_venta}. Acabados: {", ".join(insumo.nombre for insumo in venta.insumos.all())}. Total: {venta.total_venta}',
                total=venta.total_venta,
            )
            factura.save()
    else:
        # Verifica si ya existe un recibo para esta venta
        recibo_existente = Recibo.objects.filter(
            tipo="Servicio",
            detalle__icontains=f"Detalle del recibo {venta.id_venta}",
        ).first()

        if recibo_existente:
            # Actualiza el total del recibo existente
            recibo_existente.total = venta.total_venta
            recibo_existente.save()
        else:
            # Crea el recibo
            recibo = Recibo(
                tipo="Servicio",

                detalle=f'Cliente: {venta.cliente.nombre + venta.cliente.apellidos}. Acabados: {", ".join(insumo.nombre for insumo in venta.insumos.all())}. Total: {venta.total_venta}',
                total=venta.total_venta,
            )
            

            # Guarda el recibo después de enviar el mensaje
            recibo.save()

    # Actualiza el stock de insumos en el inventario
    for insumo in venta.insumos.all():
        stock, created = StockInsumo.objects.get_or_create(
            inventario=venta.inventario, insumo=insumo
        )
        # Asegúrate de ajustar según tu lógica de cómo se debe restar la cantidad
        # En este caso, la cantidad de insumos se puede obtener directamente desde el modelo StockInsumo
        cantidad = stock.cantidad
        stock.cantidad -= cantidad
        stock.save()

    venta.save()

    # Agrega mensajes de depuración para verificar la ejecución
    print("Stock y totales actualizados correctamente.")



class ResultadoAnalisis(models.Model):
    id_resultado = models.CharField(
        primary_key=True,
        max_length=100,
        unique=True,
        default=conver_encode,
        editable=False,
    )
    fecha_analisis = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha del análisis"
    ) 
    resultado = models.JSONField(verbose_name="Resultado")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_resultado

    class Meta:
        verbose_name = "Analisis de predicciones"
        verbose_name_plural = "Analisis de predicciones"
        db_table = "resultado_analisis"
        ordering = ['-fecha_analisis'] 
        
import json
import re
from django.db.models import Sum,Count




@receiver(post_save, sender=Venta)
def analizar_venta(sender, instance, **kwargs):
        load_dotenv()
    
        # Configurar la API de PALM con tu clave de API
        google_api_key = os.environ.get("GOOGLE_API_KEY")
        palm.configure(api_key=google_api_key)

        # Modelos disponibles
        models = [ m  for m in palm.list_models()if "generateText" in m.supported_generation_methods ]
        model = models[0].name  # Puedes ajustar según tus preferencias

        # Recuperar datos relevantes de las tablas
        clientes = Cliente.objects.all()[:15]
        ventas = Venta.objects.select_related("cliente").all()[:15]
        cotizaciones = Cotizacion.objects.all()[:15]
        facturas = Factura.objects.filter(tipo="Servicio")[:15]
        recibos = Recibo.objects.all()[:15]
        insumos = Insumo.objects.all()
        print("Recuperando datos...")

        # Datos de clientes
        datos_clientes = [{"nombre": cliente.nombre, "correo": cliente.correo_electronico} for cliente in clientes]

        # Datos de ventas
        datos_ventas = [{"cliente": venta.cliente.nombre, "total": venta.total_venta, "fecha": venta.created_at} for venta in ventas]

        # Datos de cotizaciones
        datos_cotizaciones = [{"cliente": cotizacion.cliente.nombre, "total_cotizacion": cotizacion.total, "fecha": cotizacion.created_at} for cotizacion in cotizaciones]

        # Datos de facturas y recibos
        datos_facturas = [{"total": factura.total, "fecha": factura.created_at} for factura in facturas]
        datos_recibos = [{"total": recibo.total, "fecha": recibo.created_at} for recibo in recibos]

        # Datos de insumos
        datos_insumos = [{"nombre": insumo.nombre, "precio": insumo.precio, "categoria": insumo.categoria} for insumo in insumos]

        for cliente_data in datos_clientes:
            total_spending = sum(venta["total"] for venta in datos_ventas if venta["cliente"] == cliente_data["nombre"])
            cliente_data["total_spending"] = total_spending

        prompt = (
            "Predictive Sales Forecast for Future Demand (in Bolivianos - Bs):\n"
            f"- Total Sales Trend Analysis: Evaluate the trend based on a total sales sum of {sum(venta['total'] for venta in datos_ventas)} Bs.\n"
            f"- Customer Spending Patterns: Analyze the spending patterns from {len(datos_clientes)} customers, focusing on the total spendings calculated as {sum(cliente['total_spending'] for cliente in datos_clientes)} Bs.\n"
            f"- Product Performance Evaluation: Assess the performance of products based on their current sales and categories, expressed in Bs. For example, product '{datos_ventas[0]['cliente']}' generated Bs {datos_ventas[0]['total']} in sales.\n"
            f"- Total Quotations: Analyze the total quotations summing up to {sum(cotizacion['total_cotizacion'] for cotizacion in datos_cotizaciones)} Bs.\n"
            f"- Total Invoices: Evaluate the total revenue generated from invoices, which is {sum(factura['total'] for factura in datos_facturas)} Bs.\n"
            f"- Total Receipts: Assess the total amount received from receipts, which is {sum(recibo['total'] for recibo in datos_recibos)} Bs.\n"
            f"- Total Supplies: Analyze the total cost of supplies, which amounts to {sum(insumo['precio'] for insumo in datos_insumos)} Bs.\n"
            "Forecast Objectives:\n"
            "- Project the sales trend into the next year, considering current economic factors, and express this in Bolivianos.\n"
            "- Identify key customer segments based on spending habits for targeted marketing strategies, with spendings evaluated in Bs.\n"
            "- Predict future demand for top-performing products and suggest inventory strategies, with all predictions and recommendations made in terms of Bolivianos.\n"
        )
        print("Preparando el prompt para la generación de texto...")

        print("Generando texto con PALM...")
        # Llamar a la API de PALM para obtener el resultado en texto
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0.5,
            max_output_tokens=500,
        )
        print("Texto generado.")
        print("Traduciendo el resultado...")
        # Traducir el resultado obtenido a español en chunks
        translator = EasyGoogleTranslate(
            source_language='en',
            target_language='es',
            timeout=10
        )
        print("Resultado traducido.")

        chunk_size = 200  # Puedes ajustar el tamaño del chunk según tus necesidades
        resultado_traducido = ""
        for i in range(0, len(completion.result), chunk_size):
            chunk = completion.result[i : i + chunk_size]
            resultado_traducido += translator.translate(chunk)

        print("Convirtiendo el resultado a JSON y almacenando en la base de datos...")
        # Convertir el resultado traducido a formato JSON
        json_result = {
            "result": {
                "generated_text": resultado_traducido.strip()
                .replace("*", "")
                .replace("\n", ""),
            }
        }
     

        print("Resultado almacenado en la base de datos.")
        # Guardar el resultado en la base de datos
        resultado_analisis = ResultadoAnalisis(
            resultado=json_result
        )
        resultado_analisis.save()



@receiver(post_save, sender=Venta)
def asignar_fase_pendiente(sender, instance, **kwargs):
    # Verifica si la venta no tiene una fase asociada al cliente
    if not instance.cliente.fases.filter(fase="Pendiente").exists():
        # Crea una nueva fase "Pendiente" y asígnala al cliente
        Fase.objects.create(cliente=instance.cliente, fase="Pendiente")



@receiver(post_save, sender=Fase)
def enviar_mensaje_whatsapp(sender, instance, **kwargs):
    if kwargs.get('created', False) or kwargs.get('update_fields', None):
        #cliente = instance.cliente  # Obtén el cliente relacionado
        #if cliente:
        #    numero_whatsapp = cliente.celular  # Obtiene el número de WhatsApp del cliente
        #    mensaje = f"Hola te encuentras en la fase: {instance.fase}, de tu servicio de imprenta. Te estaremos informando el proceso de tu pedido gracias."
        #    pywhatkit.sendwhatmsg_instantly(numero_whatsapp, mensaje)
        # personalizando     mensajes segun la fase
        if (instance.fase=='Pendiente'):
            mensaje = f"Hola te encuentras en la fase: {instance.fase}, de tu servicio de imprenta. Te estaremos informando el proceso de tu pedido gracias."
        elif (instance.fase=='Rayado y corte'):
            mensaje = f"Hola te encuentras en la fase: {instance.fase}, ya estamos en la segunda fase. Te estaremos informando el proceso de tu pedido gracias."
        elif (instance.fase=='Impresion'):
            mensaje = f"Hola te encuentras en la fase: {instance.fase}, Nos encontramos imprimiendo. Te estaremos informando el proceso de tu pedido gracias."
        elif (instance.fase=='Acabado final'):
            mensaje = f"Hola te encuentras en la fase: {instance.fase}, ya esta Listo!, puedes pasar a recoger."
        elif (instance.fase=='Entregado'):
            mensaje = f"Cumplimos!: {instance.fase},gracias por adquirir nuestros servicios te esperamos pronto."
        numero_whatsapp = "+59170693215" 
        pywhatkit.sendwhatmsg_instantly(numero_whatsapp, mensaje)


@receiver(pre_save, sender=Fase)
def enviar_mensaje_whatsapp(sender, instance, **kwargs):
    #cliente = instance.cliente  # Obtén el cliente relacionado
        #if cliente:
        #    numero_whatsapp = cliente.celular  # Obtiene el número de WhatsApp del cliente
        #    mensaje = f"Hola te encuentras en la fase: {instance.fase}, de tu servicio de imprenta. Te estaremos informando el proceso de tu pedido gracias."
        #    pywhatkit.sendwhatmsg_instantly(numero_whatsapp, mensaje)
     # personalizando     mensajes segun la fase
    if (instance.fase=='Pendiente'):
        mensaje = f"Hola te encuentras en la fase: {instance.fase}, de tu servicio de imprenta. Te estaremos informando el proceso de tu pedido gracias."
    elif (instance.fase=='Rayado y corte'):
        mensaje = f"Hola te encuentras en la fase: {instance.fase}, ya estamos en la segunda fase. Te estaremos informando el proceso de tu pedido gracias."
    elif (instance.fase=='Impresion'):
        mensaje = f"Hola te encuentras en la fase: {instance.fase}, Nos encontramos imprimiendo. Te estaremos informando el proceso de tu pedido gracias."
    elif (instance.fase=='Acabado final'):
        mensaje = f"Hola te encuentras en la fase: {instance.fase}, ya esta Listo!, puedes pasar a recoger."
    elif (instance.fase=='Entregado'):
        mensaje = f"Cumplimos!: {instance.fase},gracias por adquirir nuestros servicios te esperamos pronto."
    numero_whatsapp = "+59170693215"  
    pywhatkit.sendwhatmsg_instantly(numero_whatsapp, mensaje)