from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import TemplateView
from apps.ventas.models import Factura,Recibo,ResultadoAnalisis,Cliente,Cotizacion,Venta,Fase
from apps.empresa.models import Sucursal,Servicio,Inventario
from apps.compras.models import Compra,Insumo,Proveedor
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Sum
from django.views.generic.edit import CreateView
from apps.ventas.forms import VentaForm,ClienteForm,CotizacionForm,FaseForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.http import Http404
from apps.empresa.forms import SucursalForm,InventarioForm,ServicioForm,UserForm
from apps.compras.forms import CompraForm,DetalleCompraForm,InsumoForm,ProveedorForm


class  Inicio(LoginRequiredMixin,TemplateView):
    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total de ventas
        context['total_ventas'] = Venta.objects.aggregate(total=Sum('total_venta'))['total'] or 0

        # Total de clientes
        context['total_clientes'] = Cliente.objects.count()

        # Total de servicios
        context['total_servicios'] = Servicio.objects.count()

        # Total de sucursales
        context['total_sucursales'] = Sucursal.objects.count()

        context['top_insumos'] = Venta.objects.values('insumos__nombre') \
                                    .annotate(total_usos=Count('insumos')) \
                                    .order_by('-total_usos')[:5]
        
        context['top_clientes'] = Venta.objects.values('cliente__nombre', 'cliente__apellidos') \
                                    .annotate(total_ventas=Sum('total_venta')) \
                                    .order_by('-total_ventas')[:5]
        
        ventas_por_mes = Venta.objects.annotate(mes=TruncMonth('created_at')) \
                            .values('mes') \
                            .annotate(total_ventas_mes=Sum('total_venta')) \
                            .order_by('mes')

        context['ventas_por_mes'] = list(ventas_por_mes)



        return context


class ResultadoAnalisis(LoginRequiredMixin,ListView):
    model = ResultadoAnalisis
    template_name = "pages/analisis.html"
    context_object_name = 'analisis'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().order_by('-fecha_analisis')

class EditarUsuario(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']  # Puedes ajustar los campos según tus necesidades
    template_name = "pages/usuarios/edit.html"
    context_object_name = 'usuario'
    success_url = reverse_lazy('web:usuarios')  # Redirecciona aquí después de editar
   
    def get_object(self):
        # Asegura que el usuario solo pueda editar su propio perfil
        if self.kwargs.get('pk') != self.request.user.pk:
            raise Http404("No puedes editar otros perfiles.")
        return self.request.user
    
def crear_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('web:sucursales')  # Redirige a la lista de sucursales o a donde prefieras
    else:
        form = SucursalForm()
    
    return render(request, 'pages/sucursales/crear.html', {'form': form})

def crear_usuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Iniciar sesión automáticamente después de crear un usuario
            login(request, user)
            return redirect('web:usuarios')  # Cambia 'web:inicio' por la URL de inicio de tu aplicación
    else:
        form = UserForm()
    return render(request, 'pages/usuarios/crear.html', {'form': form})


def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('web:proveedores')  # Redirige a la lista de proveedores (ajusta la URL según tu configuración)
    else:
        form = ProveedorForm()
    
    return render(request, 'pages/provedores/crear.html', {'form': form})

def editar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)

    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('web:proveedores')  # Redirige a la lista de proveedores (ajusta la URL según tu configuración)
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'pages/provedores/edit.html', {'form': form, 'proveedor': proveedor})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('web:clientes')  # Redirige a la lista de clientes (ajusta la URL según tu configuración)
    else:
        form = ClienteForm()
    
    return render(request, 'pages/clientes/crear.html', {'form': form})

def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('web:clientes')  # Redirige a la lista de clientes (ajusta la URL según tu configuración)
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'pages/clientes/edit.html', {'form': form, 'cliente': cliente})

def crear_cotizacion(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            cotizacion = form.save()
            # Realiza aquí cualquier procesamiento adicional necesario
            return redirect('web:cotizaciones')  # Redirige a la lista de cotizaciones (ajusta la URL según tu configuración)
    else:
        form = CotizacionForm()
    
    return render(request, 'pages/cotizaciones/crear.html', {'form': form})

def editar_fase(request, id_fase):
    fase = get_object_or_404(Fase, id_fase=id_fase)
    
    if request.method == 'POST':
        form = FaseForm(request.POST, instance=fase)
        if form.is_valid():
            form.save()
            return redirect('web:fases')  # Redirige a donde quieras después de editar
    else:
        form = FaseForm(instance=fase)
    
    return render(request, 'pages/procesos/edit.html', {'form': form, 'fase': fase})

def crear_inventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('web:inventarios')  # Redirecciona a la lista de inventarios después de la creación
    else:
        form = InventarioForm()
    
    return render(request, 'pages/inventario/crear.html', {'form': form})


class FasesListView(LoginRequiredMixin, ListView):
    model = Fase
    template_name = "pages/procesos/procesos.html"  # Ajusta la ruta de tu template
    context_object_name = 'fases'  # Nombre de la variable en el contexto
    paginate_by = 10 

def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('web:servicios')  # Cambia 'web:servicios' por la URL de la lista de servicios
    else:
        form = ServicioForm()

    return render(request, 'pages/servicios/crear.html', {'form': form})

def crear_compra(request):
    if request.method == 'POST':
        compra_form = CompraForm(request.POST)
        detalle_formset = DetalleCompraForm(request.POST, prefix='detalle')  # Utiliza DetalleCompraFormSet
        if compra_form.is_valid() and detalle_formset.is_valid():
            compra = compra_form.save(commit=False)
            detalle_formset.instance = compra  # Asigna la compra al detalle antes de guardarlo
            compra.save()  # Guarda la compra antes de guardar los detalles
            detalle_formset.save()  # Guarda los detalles de la compra

            # Calcula el total de la compra
            total_compra = 0
            detalles = compra.detalles.all()
            for detalle in detalles:
                total_compra += detalle.insumo.precio * detalle.cantidad
            compra.total_compra = total_compra
            compra.save()

            return redirect('web:compras')  # Cambia 'web:compras' por la URL de la lista de compras
    else:
        compra_form = CompraForm()
        detalle_formset = DetalleCompraForm(prefix='detalle')

    return render(request, 'pages/compras/crear.html', {'compra_form': compra_form, 'detalle_formset': detalle_formset})


def crear_insumo(request):
    if request.method == 'POST':
        insumo_form = InsumoForm(request.POST)
        if insumo_form.is_valid():
            insumo = insumo_form.save()
            return redirect('web:insumos')  # Cambia 'web:insumos' por la URL de la lista de insumos
    else:
        insumo_form = InsumoForm()

    return render(request, 'pages/insumos/crear.html', {'insumo_form': insumo_form})

def editar_insumo(request, id_insumo):
    insumo = get_object_or_404(Insumo, id_insumo=id_insumo)
    
    if request.method == 'POST':
        insumo_form = InsumoForm(request.POST, instance=insumo)
        if insumo_form.is_valid():
            insumo_form.save()
            return redirect('web:insumos')  # Redirige a la lista de insumos o a donde desees
    else:
        insumo_form = InsumoForm(instance=insumo)
    
    context = {
        'insumo_form': insumo_form,
    }
    
    return render(request, 'pages/insumos/edit.html', context)



class EditarSucursal(LoginRequiredMixin, UpdateView):
    model = Sucursal
    fields = ['nombre', 'direccion', 'latitud', 'longitud']  # Ajusta los campos según tus necesidades
    template_name = "pages/sucursales/edit.html"
    context_object_name = 'sucursal'
    success_url = reverse_lazy('web:sucursales')  # Redirecciona aquí después de editar

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = super().get_object(queryset=queryset)
        # Aquí puedes añadir lógica adicional si necesitas
        return obj



class Facturas(LoginRequiredMixin,ListView):
    model = Factura
    template_name = "pages/facturas/facturas.html"
    context_object_name = 'facturas'
    paginate_by = 10

class Recibos(LoginRequiredMixin,ListView):
    model = Recibo
    template_name = "pages/recibos/recibos.html"
    context_object_name = 'recibos'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class Clientes(LoginRequiredMixin,ListView):
    model = Cliente
    template_name = "pages/clientes/clientes.html"
    context_object_name = 'clientes'
    paginate_by = 10

class Cotizaciones(LoginRequiredMixin,ListView):
    model = Cotizacion
    template_name = "pages/cotizaciones/cotizaciones.html"
    context_object_name = 'cotizaciones'
    paginate_by = 10

class Ventas(LoginRequiredMixin,ListView):
    model = Venta
    template_name = "pages/ventas/ventas.html"
    context_object_name = 'ventas'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class RegistrarVenta(LoginRequiredMixin,CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'pages/ventas/crear_venta.html'
    success_url = reverse_lazy('web:ventas')

    def form_valid(self, form):
        # Aquí puedes imprimir los datos del formulario para depuración
        print(form.cleaned_data)
        return super().form_valid(form)

  

class Sucursales(LoginRequiredMixin,ListView):
    model = Sucursal
    template_name = "pages/sucursales/sucursales.html"
    context_object_name = 'sucursales'
    paginate_by = 10

class Servicios(LoginRequiredMixin,ListView):
    model = Servicio
    template_name = "pages/servicios/servicios.html"
    context_object_name = 'servicios'
    paginate_by = 10


class Inventarios(LoginRequiredMixin,ListView):
    model = Inventario
    template_name = "pages/inventario/inventarios.html"
    context_object_name = 'inventarios'
    paginate_by = 10


class Compras(LoginRequiredMixin,ListView):
    model = Compra
    template_name = "pages/compras/compras.html"
    context_object_name = 'compras'
    paginate_by = 10


class Insumos(LoginRequiredMixin,ListView):
    model = Insumo
    template_name = "pages/insumos/insumos.html"
    context_object_name = 'insumos'
    paginate_by = 10

class Proveedores(LoginRequiredMixin,ListView):
    model = Proveedor
    template_name = "pages/provedores/provedores.html"
    context_object_name = 'proveedores'
    paginate_by = 10

class Usuarios(LoginRequiredMixin,ListView):
    model = User
    template_name = 'pages/usuarios/usuarios.html'  # Asegúrate de crear esta plantilla
    context_object_name = 'usuarios'
    paginate_by = 10

def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado con éxito.')
        return redirect('web:usuarios')

    return render(request, 'pages/usuarios/usuarios.html', {'usuario': usuario})


def eliminar_fase(request, id_fase):
    fase = get_object_or_404(Fase, id_fase=id_fase)

    if request.method == 'POST':
        fase.delete()
        messages.success(request, 'Fase eliminado con éxito.')
        return redirect('web:fases')

    return render(request, 'pages/procesos/procesos.html', {'fase': fase})

def eliminar_inventario(request, id_inventario):
    inventario = get_object_or_404(Inventario, id_inventario=id_inventario)

    if request.method == 'POST':
        inventario.delete()
        messages.success(request, 'Inventario eliminado con éxito.')
        return redirect('web:inventarios')

    return render(request, 'pages/inventario/inventarios.html', {'inventario': inventario})


def eliminar_servicio(request, id_servicio):
    servicio = get_object_or_404(Servicio, id_servicio=id_servicio)

    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado con éxito.')
        return redirect('web:servicios')

    return render(request, 'pages/servicios/servicios.html', {'servicio': servicio})


def eliminar_sucursal(request, id_sucursal):
    sucursal = get_object_or_404(Sucursal, id_sucursal=id_sucursal)

    if request.method == 'POST':
        sucursal.delete()
        messages.success(request, 'Sucursal eliminado con éxito.')
        return redirect('web:sucursales')

    return render(request, 'pages/sucursales/sucursales.html', {'sucursal': sucursal})

def eliminar_compra(request, id_compra):
    compra = get_object_or_404(Compra, id_compra=id_compra)

    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'Compra eliminado con éxito.')
        return redirect('web:compras')

    return render(request, 'pages/compras/compras.html', {'compra': compra})

def eliminar_insumo(request, id_insumo):
    insumo = get_object_or_404(Insumo, id_insumo=id_insumo)

    if request.method == 'POST':
        insumo.delete()
        messages.success(request, 'Insumo eliminado con éxito.')
        return redirect('web:insumos')

    return render(request, 'pages/insumos/insumos.html', {'insumo': insumo})

def eliminar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)

    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado con éxito.')
        return redirect('web:proveedores')

    return render(request, 'pages/provedores/provedores.html', {'proveedor': proveedor})

def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado con éxito.')
        return redirect('clientes')

    return render(request, 'pages/clientes/clientes.html', {'cliente': cliente})

def eliminar_cotizacion(request, id_cotizacion):
    cotizacion = get_object_or_404(Cotizacion, id_cotizacion=id_cotizacion)

    if request.method == 'POST':
        cotizacion.delete()
        messages.success(request, 'Cotizacion eliminado con éxito.')
        return redirect('web:cotizaciones')

    return render(request, 'pages/cotizaciones/cotizaciones.html', {'cotizacion': cotizacion})

def eliminar_venta(request, id_venta):
    venta = get_object_or_404(Venta, id_venta=id_venta)

    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'venta eliminado con éxito.')
        return redirect('web:ventas')

    return render(request, 'pages/ventas/ventas.html', {'venta': venta})

def eliminar_recibo(request, id_recibo):
    recibo = get_object_or_404(Recibo, id_recibo=id_recibo)

    if request.method == 'POST':
        recibo.delete()
        messages.success(request, 'Recibo eliminado con éxito.')
        return redirect('web:recibos')

    return render(request, 'pages/recibos/recibos.html', {'recibo': recibo})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('web:inicio')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('web:inicio')  # Redireccionar a la página de inicio después del inicio de sesión
        else:
            # Mensaje de error de inicio de sesión inválido
            return render(request, 'pages/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'pages/login.html')
