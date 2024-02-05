# En el archivo urls.py en tu proyecto principal
from django.urls import include, path,re_path
from django.contrib.auth.decorators import login_required
from .views import login_view,Usuarios,eliminar_venta,eliminar_fase,editar_fase,FasesListView,crear_cotizacion,editar_cliente,crear_cliente,editar_proveedor,crear_proveedor,crear_usuario,editar_insumo,crear_compra,crear_insumo,crear_servicio,crear_inventario,crear_sucursal,EditarSucursal,RegistrarVenta,EditarUsuario,eliminar_cotizacion,eliminar_cliente,eliminar_recibo,eliminar_proveedor,eliminar_insumo,eliminar_compra,eliminar_sucursal,Inicio,eliminar_servicio,eliminar_inventario,eliminar_usuario,ResultadoAnalisis,Clientes,Cotizaciones,Ventas,Facturas,Recibos,Sucursales,Servicios,Inventarios,Compras,Insumos,Proveedores
from django.contrib.auth.views import LogoutView

app_name = 'web' 

urlpatterns = [

    path('', login_view, name='login'),
    path('logout/', login_required(LogoutView.as_view(next_page="web:login")), name='logout'),
    path('dashboard', login_required(Inicio.as_view()),name='inicio'), 
    path('analisis', login_required(ResultadoAnalisis.as_view()),name='analisis'), 
    path('facturas', login_required(Facturas.as_view()),name='facturas'), 
    path('recibos', login_required(Recibos.as_view()),name='recibos'), 
    re_path(r'^recibos/eliminar/(?P<id_recibo>[-\w]+)/$', login_required(eliminar_recibo), name='eliminar_recibo'),
    path('sucursales', login_required(Sucursales.as_view()),name='sucursales'),
    re_path(r'^sucursales/eliminar/(?P<id_sucursal>[-\w]+)/$', login_required(eliminar_sucursal), name='eliminar_sucursal'),
    path('sucursales/editar/<str:pk>/', EditarSucursal.as_view(), name='editar_sucursal'),
    path('sucursales/crear/', crear_sucursal, name='crear_sucursal'),
    path('servicios', Servicios.as_view(),name='servicios'),
    re_path(r'^servicios/eliminar/(?P<id_servicio>[-\w]+)/$', login_required(eliminar_servicio), name='eliminar_servicio'),
    path('servicios/crear/', crear_servicio, name='crear_servicio'),
    path('inventarios', Inventarios.as_view(),name='inventarios'),
    re_path(r'^inventarios/eliminar/(?P<id_inventario>[-\w]+)/$', login_required(eliminar_inventario), name='eliminar_inventario'),
    path('inventarios/crear/', crear_inventario, name='crear_inventario'),
    path('compras', Compras.as_view(),name='compras'),
    re_path(r'^compras/eliminar/(?P<id_compra>[-\w]+)/$', login_required(eliminar_compra), name='eliminar_compra'),
    path('compras/crear/', crear_compra, name='crear_compra'),
    path('insumos', Insumos.as_view(),name='insumos'),
    re_path(r'^insumos/eliminar/(?P<id_insumo>[-\w]+)/$', login_required(eliminar_insumo), name='eliminar_insumo'),
    path('insumos/crear/', crear_insumo, name='crear_insumo'),
    path('insumos/editar/<str:id_insumo>/', editar_insumo, name='editar_insumo'),
    path('proveedores', Proveedores.as_view(),name='proveedores'),
    path('proveedores/editar/<str:id_proveedor>/', editar_proveedor, name='editar_proveedor'),
    re_path(r'^proveedores/eliminar/(?P<id_proveedor>[-\w]+)/$', login_required(eliminar_proveedor), name='eliminar_proveedor'),
    path('proveedores/crear/', crear_proveedor, name='crear_proveedor'),
    path('clientes', Clientes.as_view(),name='clientes'),
    re_path(r'^clientes/eliminar/(?P<id_cliente>[-\w]+)/$', login_required(eliminar_cliente), name='eliminar_cliente'),
    path('clientes/crear/', crear_cliente, name='crear_cliente'),
    path('clientes/editar/<str:id_cliente>/', editar_cliente, name='editar_cliente'),
    path('cotizaciones', Cotizaciones.as_view(),name='cotizaciones'),
    re_path(r'^cotizaciones/eliminar/(?P<id_cotizacion>[-\w]+)/$', login_required(eliminar_cotizacion), name='eliminar_cotizacion'),
    path('cotizaciones/crear/', crear_cotizacion, name='crear_cotizacion'),
    path('ventas', Ventas.as_view(),name='ventas'),
    re_path(r'^ventas/eliminar/(?P<id_venta>[-\w]+)/$', login_required(eliminar_venta), name='eliminar_venta'),
    path('ventas/registrar/', login_required(RegistrarVenta.as_view()), name='registrar_venta'),
    path('usuarios', login_required(Usuarios.as_view()),name='usuarios'),
    re_path(r'^usuarios/eliminar/(?P<id>\d+)/$', login_required(eliminar_usuario), name='eliminar_usuario'),
    path('usuarios/editar/<int:pk>/', EditarUsuario.as_view(), name='editar_usuario'),
    path('usuarios/crear', crear_usuario, name='crear_usuario'),

    path('fases', FasesListView.as_view(), name='fases'),  # Puedes ajustar la URL según tu preferencia
    path('fases/editar/<str:id_fase>/', editar_fase, name='editar_fase'),
    re_path(r'^fases/eliminar/(?P<id_fase>[-\w]+)/$', login_required(eliminar_fase), name='eliminar_fase'),

]
