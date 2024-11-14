from django.test import TestCase
from .models import Categoria, Proveedor, Usuario, Producto

class UsuarioTestCase(TestCase):
    def setUp(self):
        Usuario.objects.create(
            dni="12345678", 
            nombre="Juan", 
            apellidos="Pérez",  # Usa 'apellidos' en lugar de 'apellido'
            correo="juan.perez@example.com",
            telefono="987654321", 
            cargo="Analista", 
            area="TI", 
            edad=30, 
            foto="img/image_01.jpg"
        )

    def test_crear_usuario(self):
        usuario = Usuario.objects.get(dni="12345678")
        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.apellidos, "Pérez")  # Asegúrate de usar 'apellidos'
        self.assertEqual(usuario.correo, "juan.perez@example.com")
        self.assertEqual(usuario.telefono, "987654321")
        self.assertEqual(usuario.cargo, "Analista")
        self.assertEqual(usuario.area, "TI")
        self.assertEqual(usuario.edad, 30)

class ProductoTestCase(TestCase):
    def setUp(self):
        # Crea una categoría y un proveedor para usarlos en la prueba
        categoria = Categoria.objects.create(nombre="Electrónica")
        proveedor = Proveedor.objects.create(
            ruc="123456789",
            nombre="Proveedor S.A.",
            contacto="contacto@proveedor.com",
            direccion="Calle Ejemplo 123",
            telefono="987654321",
            correo="correo@proveedor.com"
        )
        
        # Ahora crea un producto con la categoría y el proveedor creados
        self.producto = Producto.objects.create(
            serie="ABC123", 
            nombre="Laptop", 
            descripcion="Laptop para programación",
            precio=1500.00,
            stock=10,
            categoria=categoria,  # Asigna la categoría
            proveedor=proveedor   # Asigna el proveedor
        )

    def test_actualizar_producto(self):
        self.producto.stock = 15
        self.producto.save()

        producto_actualizado = Producto.objects.get(serie="ABC123")
        self.assertEqual(producto_actualizado.stock, 15)
        
        
class ProveedorTestCase(TestCase):
    def setUp(self):
        # Crear un proveedor de prueba
        Proveedor.objects.create(
            ruc="12345678901",
            nombre="Proveedor de Prueba",
            contacto="Juan Pérez",
            direccion="Calle Falsa 123",
            telefono="987654321",
            correo="prueba@proveedor.com"
        )

    def test_proveedor_creacion(self):
        # Recuperar el proveedor recién creado
        proveedor = Proveedor.objects.get(ruc="12345678901")
        
        # Verificar que los datos son correctos
        self.assertEqual(proveedor.nombre, "Proveedor de Prueba")
        self.assertEqual(proveedor.contacto, "Juan Pérez")
        self.assertEqual(proveedor.direccion, "Calle Falsa 123")
        self.assertEqual(proveedor.telefono, "987654321")
        self.assertEqual(proveedor.correo, "prueba@proveedor.com")

    def test_proveedor_str(self):
        # Verificar la representación en cadena del proveedor
        proveedor = Proveedor.objects.get(ruc="12345678901")
        self.assertEqual(str(proveedor), "Proveedor de Prueba")