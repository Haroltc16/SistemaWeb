from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.views.decorators.cache import never_cache
from .models import Almacen, Categoria, Cliente, Inventario, Producto, Proveedor, Usuario, Venta
from .forms import LoginForm, VentaForm
from django.http import Http404
from django.http import JsonResponse
from .models import Producto
from django.db.models import Count
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json

from Programa import models


# VISTAS PRINCIPALES.
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            dni = form.cleaned_data.get('username')  # Usando el campo 'dni' como username
            password = form.cleaned_data.get('password')
            
            # Autenticando al usuario
            user = authenticate(request, username=dni, password=password)

            if user is not None:
                # Loguear al usuario si las credenciales son válidas
                login(request, user)

                # Verificar a qué grupo pertenece el usuario y redirigir
                if user.groups.filter(name='Administrador').exists():
                    return redirect('admin_dashboard')
                elif user.groups.filter(name='Vendedor').exists():
                    return redirect('vendedor_dashboard')
                else:
                    return HttpResponse("El usuario no tiene un grupo asignado.")
            else:
                # Si la autenticación falla
                return render(request, 'login.html', {'form': form, 'error': 'DNI o contraseña incorrectos.'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

#############################################################################

#VISTAS ADMINISTRADOR
@never_cache
@login_required
def admin_dashboard(request):
    return render(request, 'administrador/admin_dashboard.html')

def datos_productos_por_categoria(request):
    # Obtener la cantidad de productos por cada categoría
    datos = Producto.objects.values('categoria__nombre').annotate(total=Count('categoria'))
    return JsonResponse(list(datos), safe=False)

def datos_inventario_por_almacen(request):
    # Obtener la cantidad total de productos en cada almacén
    datos = Inventario.objects.values('almacen__nombre').annotate(total=Sum('cantidad'))
    return JsonResponse(list(datos), safe=False)

#ADMIN - CATEGORIA
def listar_categorias(request):
    query = request.GET.get('q')  # Obtiene el término de búsqueda desde el formulario
    if query:
        categorias = Categoria.objects.filter(nombre__icontains=query)  # Filtra por el nombre de la categoría
    else:
        categorias = Categoria.objects.all()  # Muestra todas las categorías si no hay búsqueda

    return render(request, 'administrador/categoria/categorias.html', {'categorias': categorias, 'query': query})

def registrar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']

        Categoria.objects.create(nombre=nombre)
        
        return redirect('categorias')  # Redirige de nuevo a la lista de categorías después de registrar

    return render(request, 'administrador/categoria/registrar_categoria.html')

def actualizar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)

    if request.method == 'POST':
        categoria.nombre = request.POST['nombre']
        categoria.save()
        return redirect('categorias')

    return render(request, 'administrador/categoria/actualizar_categoria.html', {'categoria': categoria})

def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    categoria.delete()
    return redirect('categorias')

#ADMIN - PROVEEDOR
def listar_proveedores(request):
    query = request.GET.get('q')  # Obtiene el término de búsqueda desde el formulario
    if query:
        proveedores = Proveedor.objects.filter(nombre__icontains=query)  # Filtra por el nombre
    else:
        proveedores = Proveedor.objects.all()  # Muestra todos los proveedores si no hay búsqueda

    return render(request, 'administrador/proveedor/proveedores.html', {'proveedores': proveedores, 'query': query})

def eliminar_proveedor(request, ruc):
    proveedor = get_object_or_404(Proveedor, ruc=ruc)
    proveedor.delete()
    return redirect('proveedores')

def actualizar_proveedor(request, ruc):
    proveedor = get_object_or_404(Proveedor, ruc=ruc)

    if request.method == 'POST':
        proveedor.nombre = request.POST['nombre']
        proveedor.contacto = request.POST['contacto']
        proveedor.direccion = request.POST['direccion']
        proveedor.telefono = request.POST['telefono']
        proveedor.correo = request.POST['correo']
        proveedor.save()
        return redirect('proveedores')

    return render(request, 'administrador/proveedor/actualizar_proveedor.html', {'proveedor': proveedor})

def registrar_proveedor(request):
    if request.method == 'POST':
        ruc = request.POST['ruc']
        nombre = request.POST['nombre']
        contacto = request.POST['contacto']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        
        Proveedor.objects.create(
            ruc=ruc,
            nombre=nombre,
            contacto=contacto,
            direccion=direccion,
            telefono=telefono,
            correo=correo
        )
        
        return redirect('proveedores')  # Redirige de nuevo a la lista de proveedores después de registrar
        
    return render(request, 'administrador/proveedor/registrar_proveedor.html')

#ADMIN - PRODUCTO
def listar_productos(request):
    query = request.GET.get('q')  # Obtiene el término de búsqueda desde el formulario
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)  # Filtra por el nombre del producto
    else:
        productos = Producto.objects.all()  # Muestra todos los productos si no hay búsqueda

    return render(request, 'administrador/productos/productos.html', {'productos': productos, 'query': query})

def registrar_producto(request):
    if request.method == 'POST':
        serie = request.POST['serie']
        nombre = request.POST['nombre']
        descripcion = request.POST.get('descripcion', '')
        precio = request.POST['precio']
        stock = request.POST['stock']
        categoria_id = request.POST['categoria']
        proveedor_ruc = request.POST['proveedor']

        # Validación de la categoría y el proveedor
        try:
            categoria = Categoria.objects.get(pk=categoria_id)
        except Categoria.DoesNotExist:
            raise Http404("La categoría seleccionada no existe.")

        try:
            proveedor = Proveedor.objects.get(ruc=proveedor_ruc)
        except Proveedor.DoesNotExist:
            raise Http404("El proveedor seleccionado no existe.")

        # Crear el producto si la categoría y el proveedor son válidos
        Producto.objects.create(
            serie=serie,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria,
            proveedor=proveedor
        )
        
        return redirect('productos')  # Redirige de nuevo a la lista de productos después de registrar

    # Obtener todas las categorías y proveedores para el formulario
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'administrador/productos/registrar_producto.html', {'categorias': categorias, 'proveedores': proveedores})

def actualizar_producto(request, serie):
    # Obtener el producto con la serie proporcionada o retornar 404 si no existe
    producto = get_object_or_404(Producto, serie=serie)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre', producto.nombre).strip()
        producto.descripcion = request.POST.get('descripcion', producto.descripcion).strip()
        producto.precio = request.POST.get('precio', producto.precio).strip()
        producto.stock = request.POST.get('stock', producto.stock).strip()
        categoria_id = request.POST.get('categoria', producto.categoria.categoria_id).strip()
        proveedor_ruc = request.POST.get('proveedor', producto.proveedor.ruc).strip()

        # Validar y actualizar la categoría
        try:
            categoria = Categoria.objects.get(pk=categoria_id)
            producto.categoria = categoria
        except Categoria.DoesNotExist:
            raise Http404("La categoría seleccionada no existe.")

        # Validar y actualizar el proveedor
        try:
            proveedor = Proveedor.objects.get(ruc=proveedor_ruc)
            producto.proveedor = proveedor
        except Proveedor.DoesNotExist:
            raise Http404("El proveedor seleccionado no existe.")

        # Guardar los cambios en el producto
        producto.save()
        return redirect('productos')  # Redirigir a la lista de productos

    # Obtener todas las categorías y proveedores para mostrar en el formulario
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'administrador/productos/actualizar_producto.html', {
        'producto': producto,
        'categorias': categorias,
        'proveedores': proveedores
    })

def eliminar_producto(request, serie):
    producto = get_object_or_404(Producto, serie=serie)
    producto.delete()
    return redirect('productos')

#ADMIN - INVENTARIO
def inventario_view(request):
    query = request.GET.get('q')
    if query:
        inventario = Inventario.objects.filter(almacen__nombre__icontains=query)
    else:
        inventario = Inventario.objects.all()  # Obtiene todos los registros de inventario
        
    return render(request, 'administrador/inventario/inventario.html', {'inventario': inventario})

def producto_detalle(request, serie):
    producto = get_object_or_404(Producto, serie=serie)
    inventario = Inventario.objects.filter(producto=producto) \
                                   .values('almacen__nombre') \
                                   .annotate(total_cantidad=Sum('cantidad'))
    return render(request, 'administrador/inventario/producto_detalle.html', {'producto': producto, 'inventario': inventario})

def registrar_inventario(request):
    productos = Producto.objects.all()
    almacenes = Almacen.objects.all()

    if request.method == "POST":
        serie = request.POST.get('producto_serie')  # Cambia a producto_serie
        almacen_id = request.POST.get('almacen_id')  # Cambia a almacen_id
        cantidad = request.POST.get('cantidad')

        # Validar que los campos no estén vacíos
        if not serie or not almacen_id or not cantidad:
            return render(request, 'administrador/inventario/producto_almacen.html', {
                'productos': productos,
                'almacenes': almacenes,
                'error_message': 'Por favor, complete todos los campos.'
            })

        # Obtener el producto utilizando la serie
        try:
            producto = Producto.objects.get(serie=serie)
        except Producto.DoesNotExist:
            return render(request, 'administrador/inventario/producto_almacen.html', {
                'productos': productos,
                'almacenes': almacenes,
                'error_message': 'El producto con la serie proporcionada no existe.'
            })

        # Intentar crear el inventario
        try:
            Inventario.objects.create(producto=producto, almacen_id=almacen_id, cantidad=int(cantidad))
            return redirect('inventario')  # Cambia 'lista_inventario' por el nombre de la URL que maneja la lista de inventarios
        except Exception as e:
            return render(request, 'administrador/inventario/producto_almacen.html', {
                'productos': productos,
                'almacenes': almacenes,
                'error_message': f'Error al registrar el inventario: {str(e)}'
            })

    context = {
        'productos': productos,
        'almacenes': almacenes,
    }
    return render(request, 'administrador/inventario/producto_almacen.html', context) 

#ADMIN - CLIENTE
def listar_clientes(request):
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.filter(nombre__icontains=query)
    else:
        clientes = Cliente.objects.all()

    return render(request, 'administrador/cliente/clientes.html', {'clientes': clientes, 'query': query})

def eliminar_cliente(request, dni):
    cliente = get_object_or_404(Cliente, dni=dni)
    cliente.delete()
    return redirect('clientes')

def actualizar_cliente(request, dni):
    cliente = get_object_or_404(Cliente, dni=dni)

    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.apellido = request.POST['apellido']
        cliente.direccion = request.POST['direccion']
        cliente.telefono = request.POST['telefono']
        cliente.correo = request.POST['correo']
        cliente.save()
        return redirect('clientes')

    return render(request, 'administrador/cliente/actualizar_cliente.html', {'cliente': cliente})

def registrar_cliente(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        nombre = request.POST['nombre']
        apellido =request.POST['apellido']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        correo = request.POST['correo']
        
        Cliente.objects.create(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            correo=correo
        )
        
        return redirect('clientes')  # Redirige de nuevo a la lista de clientes después de registrar
        
    return render(request, 'administrador/cliente/registrar_cliente.html')

#ADMIN - PRODUCTIVIDAD

#ADMIN - VENTAS

def ventas_grafico(request):
    # Agrupa las ventas por fecha
    ventas = Venta.objects.all()
    ventas_por_dia = {}

    for venta in ventas:
        fecha = venta.fecha_venta
        total_venta = float(venta.total())  # Convierte el total a float

        if fecha in ventas_por_dia:
            ventas_por_dia[fecha] += total_venta
        else:
            ventas_por_dia[fecha] = total_venta

    # Convertir las fechas y montos a listas para JavaScript
    fechas = [fecha.strftime('%Y-%m-%d') for fecha in sorted(ventas_por_dia.keys())]
    montos = [ventas_por_dia[fecha] for fecha in sorted(ventas_por_dia.keys())]

    context = {
        'fechas': json.dumps(fechas),  # Convierte a JSON
        'montos': json.dumps(montos)   # Convierte a JSON
    }
    return render(request, 'administrador/inventario/inventario.html', context)

def obtener_ventas(request):
    # Agrupa las ventas por fecha y cuenta cuántas ventas hay por cada fecha
    ventas = Venta.objects.values('fecha_venta').annotate(cantidad=Count('id'))

    # Formato de salida para el gráfico
    fechas = [venta['fecha_venta'].strftime('%Y-%m-%d') for venta in ventas]
    cantidades = [venta['cantidad'] for venta in ventas]

    # Pasar datos al contexto para el renderizado
    context = {
        'fechas': json.dumps(fechas),  # Convierte a JSON
        'cantidades': json.dumps(cantidades)  # Convierte a JSON
    }
    return render(request, 'administrador/inventario/inventario.html', context)

def registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas')  # Redirige al dashboard después de registrar la venta
    else:
        form = VentaForm()
    return render(request, 'administrador/ventas/registrar_ventas.html', {'form': form})

def listar_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')  # Ordena las ventas por fecha
    return render(request, 'administrador/ventas/ventas.html', {'ventas': ventas})

def actualizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'ventas/actualizar_venta.html', {'form': form})

def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    venta.delete()
    return redirect('ventas')

#ADMIN - USUARIOS
def listar_usuarios(request):
    query = request.GET.get('q')  # Obtiene el término de búsqueda desde el formulario
    if query:
        usuarios = Usuario.objects.filter(nombre__icontains=query)  # Filtra por el nombre
    else:
        usuarios = Usuario.objects.all()  # Muestra todos los usuarios si no hay búsqueda

    return render(request, 'administrador/usuario/usuarios.html', {'usuarios': usuarios, 'query': query})

def eliminar_usuario(request, dni):
    usuario = get_object_or_404(Usuario, dni=dni)
    usuario.delete()
    return redirect('usuarios')

def actualizar_usuario(request, dni):
    usuario = get_object_or_404(Usuario, dni=dni)

    if request.method == 'POST':
        usuario.nombre = request.POST['nombre']
        usuario.apellidos = request.POST['apellidos']
        usuario.correo = request.POST['correo']
        usuario.telefono = request.POST['telefono']
        usuario.cargo = request.POST['cargo']
        usuario.area = request.POST['area']
        usuario.edad = request.POST['edad']

        # Actualizar la contraseña si se proporciona una nueva
        nueva_contraseña = request.POST.get('password')
        if nueva_contraseña:
            usuario.set_password(nueva_contraseña)

        # Actualizar el grupo del usuario
        grupo_nombre = request.POST.get('grupo', None)
        if grupo_nombre:
            try:
                grupo = Group.objects.get(name=grupo_nombre)
                usuario.groups.clear()
                usuario.groups.add(grupo)
            except Group.DoesNotExist:
                pass
            
        if 'foto' in request.FILES:
            usuario.foto = request.FILES['foto']
            
        usuario.save()
        return redirect('usuarios')

    # Pasar los grupos disponibles a la plantilla
    grupos_disponibles = Group.objects.all()
    return render(request, 'administrador/usuario/actualizar_usuario.html', {
        'usuario': usuario,
        'grupos': grupos_disponibles
    })
    
def detalles_usuario(request, dni):
    usuario = get_object_or_404(Usuario, dni=dni)
    return render(request, 'administrador/usuario/detalles_usuario.html', {'usuario': usuario})

def registrar_usuario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        dni = request.POST['dni']
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        cargo = request.POST['cargo']
        area = request.POST['area']
        edad = request.POST['edad']
        password = request.POST['password']
        
        # Obtener el archivo de imagen
        foto = request.FILES.get('foto')  # Capturar el archivo de imagen

        # Crear el nuevo usuario con la contraseña encriptada
        usuario = Usuario.objects.create(
            dni=dni,
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            telefono=telefono,
            cargo=cargo,
            area=area,
            edad=edad,
            password=make_password(password),  # Encriptar la contraseña
            foto=foto  # Guardar la foto en el modelo
        )

        # Asignar grupo al usuario si se seleccionó uno
        grupo_nombre = request.POST.get('grupo', None)
        if grupo_nombre:
            try:
                grupo = Group.objects.get(name=grupo_nombre)
                usuario.groups.add(grupo)
            except Group.DoesNotExist:
                pass

        # Guardar el usuario y redirigir a la lista de usuarios
        usuario.save()
        return redirect('usuarios')

    # Obtener los grupos disponibles para mostrarlos en el formulario
    grupos_disponibles = Group.objects.all()
    return render(request, 'administrador/usuario/registrar_usuario.html', {
        'grupos': grupos_disponibles
    })
    
##############################################################################

#VISTAS VENDEDOR

@never_cache
@login_required
def vendedor_dashboard(request):
    return render(request, 'vendedor/vendedor_dashboard.html')

#VENDEDOR - CATEGORIA

#VENDEDOR - PROVEEDOR
def v_listar_proveedores(request):
    query = request.GET.get('q')  # Obtiene el término de búsqueda desde el formulario
    if query:
        proveedores = Proveedor.objects.filter(nombre__icontains=query)  # Filtra por el nombre
    else:
        proveedores = Proveedor.objects.all()  # Muestra todos los proveedores si no hay búsqueda

    return render(request, 'vendedor/proveedor/v_proveedores.html', {'proveedores': proveedores, 'query': query})

def v_eliminar_proveedor(request, ruc):
    proveedor = get_object_or_404(Proveedor, ruc=ruc)
    proveedor.delete()
    return redirect('v_proveedores')

def v_actualizar_proveedor(request, ruc):
    proveedor = get_object_or_404(Proveedor, ruc=ruc)

    if request.method == 'POST':
        proveedor.nombre = request.POST['nombre']
        proveedor.contacto = request.POST['contacto']
        proveedor.direccion = request.POST['direccion']
        proveedor.telefono = request.POST['telefono']
        proveedor.correo = request.POST['correo']
        proveedor.save()
        return redirect('v_proveedores')

    return render(request, 'vendedor/proveedor/v_actualizar_proveedor.html', {'proveedor': proveedor})

def v_registrar_proveedor(request):
    if request.method == 'POST':
        ruc = request.POST['ruc']
        nombre = request.POST['nombre']
        contacto = request.POST['contacto']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        
        Proveedor.objects.create(
            ruc=ruc,
            nombre=nombre,
            contacto=contacto,
            direccion=direccion,
            telefono=telefono,
            correo=correo
        )
        
        return redirect('v_proveedores')  # Redirige de nuevo a la lista de proveedores después de registrar
        
    return render(request, 'vendedor/proveedor/v_registrar_proveedor.html')

#VENDEDOR - PRODUCTO

def v_listar_productos(request):
    query = request.GET.get('q')  # Obtiene el término de búsqueda desde el formulario
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)  # Filtra por el nombre del producto
    else:
        productos = Producto.objects.all()  # Muestra todos los productos si no hay búsqueda

    return render(request, 'vendedor/productos/v_productos.html', {'productos': productos, 'query': query})

def v_registrar_producto(request):
    if request.method == 'POST':
        serie = request.POST['serie']
        nombre = request.POST['nombre']
        descripcion = request.POST.get('descripcion', '')
        precio = request.POST['precio']
        stock = request.POST['stock']
        categoria_id = request.POST['categoria']
        proveedor_ruc = request.POST['proveedor']

        # Validación de la categoría y el proveedor
        try:
            categoria = Categoria.objects.get(pk=categoria_id)
        except Categoria.DoesNotExist:
            raise Http404("La categoría seleccionada no existe.")

        try:
            proveedor = Proveedor.objects.get(ruc=proveedor_ruc)
        except Proveedor.DoesNotExist:
            raise Http404("El proveedor seleccionado no existe.")

        # Crear el producto si la categoría y el proveedor son válidos
        Producto.objects.create(
            serie=serie,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria,
            proveedor=proveedor
        )
        
        return redirect('v_productos')  # Redirige de nuevo a la lista de productos después de registrar

    # Obtener todas las categorías y proveedores para el formulario
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'vendedor/productos/v_registrar_producto.html', {'categorias': categorias, 'proveedores': proveedores})

def v_actualizar_producto(request, serie):
    # Obtener el producto con la serie proporcionada o retornar 404 si no existe
    producto = get_object_or_404(Producto, serie=serie)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre', producto.nombre).strip()
        producto.descripcion = request.POST.get('descripcion', producto.descripcion).strip()
        producto.precio = request.POST.get('precio', producto.precio).strip()
        producto.stock = request.POST.get('stock', producto.stock).strip()
        categoria_id = request.POST.get('categoria', producto.categoria.categoria_id).strip()
        proveedor_ruc = request.POST.get('proveedor', producto.proveedor.ruc).strip()

        # Validar y actualizar la categoría
        try:
            categoria = Categoria.objects.get(pk=categoria_id)
            producto.categoria = categoria
        except Categoria.DoesNotExist:
            raise Http404("La categoría seleccionada no existe.")

        # Validar y actualizar el proveedor
        try:
            proveedor = Proveedor.objects.get(ruc=proveedor_ruc)
            producto.proveedor = proveedor
        except Proveedor.DoesNotExist:
            raise Http404("El proveedor seleccionado no existe.")

        # Guardar los cambios en el producto
        producto.save()
        return redirect('v_productos')  # Redirigir a la lista de productos

    # Obtener todas las categorías y proveedores para mostrar en el formulario
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'vendedor/productos/v_actualizar_producto.html', {
        'producto': producto,
        'categorias': categorias,
        'proveedores': proveedores
    })

def v_eliminar_producto(request, serie):
    producto = get_object_or_404(Producto, serie=serie)
    producto.delete()
    return redirect('v_productos')

#VENDEDOR - ALMACEN

#VENDEDOR - INVENTARIO

def v_inventario_view(request):
    query = request.GET.get('q')
    if query:
        inventario = Inventario.objects.filter(almacen__nombre__icontains=query)
    else:
        inventario = Inventario.objects.all()  # Obtiene todos los registros de inventario
        
    return render(request, 'vendedor/inventario/v_inventario.html', {'inventario': inventario})

def v_producto_detalle(request, serie):
    producto = get_object_or_404(Producto, serie=serie)
    inventario = Inventario.objects.filter(producto=producto) \
                                   .values('almacen__nombre') \
                                   .annotate(total_cantidad=Sum('cantidad'))
    return render(request, 'vendedor/inventario/v_producto_detalle.html', {'producto': producto, 'inventario': inventario})

def v_registrar_inventario(request):
    productos = Producto.objects.all()
    almacenes = Almacen.objects.all()

    if request.method == "POST":
        serie = request.POST.get('producto_serie')  # Cambia a producto_serie
        almacen_id = request.POST.get('almacen_id')  # Cambia a almacen_id
        cantidad = request.POST.get('cantidad')

        # Validar que los campos no estén vacíos
        if not serie or not almacen_id or not cantidad:
            return render(request, 'vendedor/inventario/v_producto_almacen.html', {
                'productos': productos,
                'almacenes': almacenes,
                'error_message': 'Por favor, complete todos los campos.'
            })

        # Obtener el producto utilizando la serie
        try:
            producto = Producto.objects.get(serie=serie)
        except Producto.DoesNotExist:
            return render(request, 'vendedor/inventario/v_producto_almacen.html', {
                'productos': productos,
                'almacenes': almacenes,
                'error_message': 'El producto con la serie proporcionada no existe.'
            })

        # Intentar crear el inventario
        try:
            Inventario.objects.create(producto=producto, almacen_id=almacen_id, cantidad=int(cantidad))
            return redirect('v_inventario')  # Cambia 'lista_inventario' por el nombre de la URL que maneja la lista de inventarios
        except Exception as e:
            return render(request, 'vendedor/inventario/v_producto_almacen.html', {
                'productos': productos,
                'almacenes': almacenes,
                'error_message': f'Error al registrar el inventario: {str(e)}'
            })

    context = {
        'productos': productos,
        'almacenes': almacenes,
    }
    return render(request, 'vendedor/inventario/v_producto_almacen.html', context)

#VENDEDOR - CLIENTE
def v_listar_clientes(request):
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.filter(nombre__icontains=query)
    else:
        clientes = Cliente.objects.all()

    return render(request, 'vendedor/cliente/v_clientes.html', {'clientes': clientes, 'query': query})

def v_eliminar_cliente(request, dni):
    cliente = get_object_or_404(Cliente, dni=dni)
    cliente.delete()
    return redirect('v_clientes')

def v_actualizar_cliente(request, dni):
    cliente = get_object_or_404(Cliente, dni=dni)

    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.apellido = request.POST['apellido']
        cliente.direccion = request.POST['direccion']
        cliente.telefono = request.POST['telefono']
        cliente.correo = request.POST['correo']
        cliente.save()
        return redirect('v_clientes')

    return render(request, 'vendedor/cliente/v_actualizar_cliente.html', {'cliente': cliente})

def v_registrar_cliente(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        nombre = request.POST['nombre']
        apellido =request.POST['apellido']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        correo = request.POST['correo']
        
        Cliente.objects.create(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            correo=correo
        )
        
        return redirect('v_clientes')  # Redirige de nuevo a la lista de clientes después de registrar
        
    return render(request, 'vendedor/cliente/v_registrar_cliente.html')

#VENDEDOR - PRODUCTIVIDAD

#VENDEDOR - VENTAS
def v_ventas_grafico(request):
    # Agrupa las ventas por fecha
    ventas = Venta.objects.all()
    ventas_por_dia = {}

    for venta in ventas:
        fecha = venta.fecha_venta
        total_venta = float(venta.total())  # Convierte el total a float

        if fecha in ventas_por_dia:
            ventas_por_dia[fecha] += total_venta
        else:
            ventas_por_dia[fecha] = total_venta

    # Convertir las fechas y montos a listas para JavaScript
    fechas = [fecha.strftime('%Y-%m-%d') for fecha in sorted(ventas_por_dia.keys())]
    montos = [ventas_por_dia[fecha] for fecha in sorted(ventas_por_dia.keys())]

    context = {
        'fechas': json.dumps(fechas),  # Convierte a JSON
        'montos': json.dumps(montos)   # Convierte a JSON
    }
    return render(request, 'vendedor/inventario/v_inventario.html', context)

def v_obtener_ventas(request):
    # Agrupa las ventas por fecha y cuenta cuántas ventas hay por cada fecha
    ventas = Venta.objects.values('fecha_venta').annotate(cantidad=Count('id'))

    # Formato de salida para el gráfico
    fechas = [venta['fecha_venta'].strftime('%Y-%m-%d') for venta in ventas]
    cantidades = [venta['cantidad'] for venta in ventas]

    # Pasar datos al contexto para el renderizado
    context = {
        'fechas': json.dumps(fechas),  # Convierte a JSON
        'cantidades': json.dumps(cantidades)  # Convierte a JSON
    }
    return render(request, 'vendedor/inventario/v_inventario.html', context)

def v_registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('v_ventas')  # Redirige al dashboard después de registrar la venta
    else:
        form = VentaForm()
    return render(request, 'vendedor/ventas/v_registrar_ventas.html', {'form': form})

def v_listar_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')  # Ordena las ventas por fecha
    return render(request, 'vendedor/ventas/v_ventas.html', {'ventas': ventas})

def v_actualizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('v_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'vendedor/ventas/v_actualizar_venta.html', {'form': form})

def v_eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    venta.delete()
    return redirect('v_ventas')


###############################################################################