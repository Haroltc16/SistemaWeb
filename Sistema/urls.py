from django.contrib import admin
from django.urls import path
from Programa import views
from django.conf.urls.static import static
from Sistema import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Página principal
    path('login/', views.login_view, name='login'),  # Pestaña de iniciar sesión
    path('logout/', views.logout_view, name='logout'),
    
    #ADMINISTRADOR
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('datos_productos_por_categoria/', views.datos_productos_por_categoria, name='datos_productos_por_categoria'),
    path('datos_inventario_por_almacen/', views.datos_inventario_por_almacen, name='datos_inventario_por_almacen'),
    path('obtener_ventas/', views.obtener_ventas, name='obtener_ventas'),
    
    #INVENTARIO
    path('registrar_inventario/', views.registrar_inventario, name='registrar_inventario'),
    path('administrador/producto/<str:serie>/', views.producto_detalle, name='producto_detalle'),
    
    #VENTA
    path('registrar/', views.registrar_venta, name='registrar_venta'),
    path('ventas/', views.listar_ventas, name='ventas'),
    path('actualizar/<int:venta_id>/', views.actualizar_venta, name='actualizar_venta'),
    path('eliminar/<int:venta_id>/', views.eliminar_venta, name='eliminar_venta'),
    path('administrador/ventas/', views.ventas_grafico, name='ventas_grafico'),

    
    #CATEGORIA
    path('categorias/', views.listar_categorias, name='categorias'),
    path('categoria/nueva/', views.registrar_categoria, name='registrar_categoria'),
    path('categoria/editar/<int:categoria_id>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('categoria/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    
    #PRODUCTOS
    path('productos/', views.listar_productos, name='productos'),
    path('producto/nuevo/', views.registrar_producto, name='registrar_producto'),
    path('producto/editar/<str:serie>/', views.actualizar_producto, name='actualizar_producto'),
    path('producto/eliminar/<str:serie>/', views.eliminar_producto, name='eliminar_producto'),
    
    #CLIENTE
    path('clientes/', views.listar_clientes, name='clientes'),
    path('clientes/nuevo/', views.registrar_cliente, name='registrar_cliente'),
    path('clientes/actualizar/<str:dni>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/eliminar/<str:dni>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    #PROVEEDOR
    path('proveedores/', views.listar_proveedores, name='proveedores'),
    path('proveedores/eliminar/<str:ruc>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedores/actualizar/<str:ruc>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/nuevo/', views.registrar_proveedor, name='registrar_proveedor'),
    
    #USUARIOS
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('usuarios/registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/actualizar/<str:dni>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/eliminar/<str:dni>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/detalle/<str:dni>/', views.detalles_usuario, name='usuario_detalle'),
    
    
    #VENDEDOR
    path('vendedor-dashboard/', views.vendedor_dashboard, name='vendedor_dashboard'),
    path('v_obtener_ventas/', views.v_obtener_ventas, name='v_obtener_ventas'),
    
    #INVENTARIO
    path('v_registrar_inventario/', views.v_registrar_inventario, name='v_registrar_inventario'),
    path('v_vendedor/producto/<str:serie>/', views.v_producto_detalle, name='v_producto_detalle'),
    
    #VENTA
    path('v_registrar/', views.v_registrar_venta, name='v_registrar_venta'),
    path('v_ventas/', views.v_listar_ventas, name='v_ventas'),
    path('v_actualizar/<int:venta_id>/', views.v_actualizar_venta, name='v_actualizar_venta'),
    path('v_eliminar/<int:venta_id>/', views.v_eliminar_venta, name='v_eliminar_venta'),
    path('v_vendedor/ventas/', views.v_ventas_grafico, name='v_ventas_grafico'),

    
    #CATEGORIA
    path('categorias/', views.listar_categorias, name='categorias'),
    path('categoria/nueva/', views.registrar_categoria, name='registrar_categoria'),
    path('categoria/editar/<int:categoria_id>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('categoria/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    
    #PRODUCTOS
    path('v_productos/', views.v_listar_productos, name='v_productos'),
    path('v_producto/nuevo/', views.v_registrar_producto, name='v_registrar_producto'),
    path('v_producto/editar/<str:serie>/', views.v_actualizar_producto, name='v_actualizar_producto'),
    path('v_producto/eliminar/<str:serie>/', views.v_eliminar_producto, name='v_eliminar_producto'),
    
    #CLIENTE
    path('v_clientes/', views.v_listar_clientes, name='v_clientes'),
    path('v_clientes/nuevo/', views.v_registrar_cliente, name='v_registrar_cliente'),
    path('v_clientes/actualizar/<str:dni>/', views.v_actualizar_cliente, name='v_actualizar_cliente'),
    path('v_clientes/eliminar/<str:dni>/', views.v_eliminar_cliente, name='v_eliminar_cliente'),
    
    #PROVEEDOR
    path('v_proveedores/', views.v_listar_proveedores, name='v_proveedores'),
    path('v_proveedores/eliminar/<str:ruc>/', views.v_eliminar_proveedor, name='v_eliminar_proveedor'),
    path('v_proveedores/actualizar/<str:ruc>/', views.v_actualizar_proveedor, name='v_actualizar_proveedor'),
    path('v_proveedores/nuevo/', views.v_registrar_proveedor, name='v_registrar_proveedor'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)