from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, dni, nombre, apellidos, correo, telefono, cargo, area, edad, password=None):
        if not dni:
            raise ValueError('El usuario debe tener un DNI')

        user = self.model(
            dni=dni,
            nombre=nombre,
            apellidos=apellidos,
            correo=self.normalize_email(correo),
            telefono=telefono,
            cargo=cargo,
            area=area,
            edad=edad,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, nombre, apellidos, correo, telefono, cargo, area, edad, password=None):
        user = self.create_user(
            dni=dni,
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            telefono=telefono,
            cargo=cargo,
            area=area,
            edad=edad,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True  # Es importante para el acceso al admin
        user.is_superuser = True  # Asegúrate de establecer esto también
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    dni = models.CharField(primary_key=True, max_length=8, unique=True)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=9)
    cargo = models.CharField(max_length=15)  # Nuevo campo para el cargo
    area = models.CharField(max_length=20, default="Area de TI")   # Nuevo campo para el área
    edad = models.PositiveIntegerField()     # Nuevo campo para la edad
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)  # Nuevo campo para la foto

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'correo', 'telefono', 'cargo', 'area', 'edad']

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def has_perm(self, perm, obj=None):
        # Aquí puedes implementar lógica adicional para los permisos si es necesario
        return True

    def has_module_perms(self, app_label):
        # Aquí puedes implementar lógica adicional para los módulos si es necesario
        return True
    


#TABLAS DE LA BASE DE DATOS RELACIONAL

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre 
    

class Proveedor(models.Model):
    ruc = models.CharField(max_length=11, primary_key=True)  # RUC como PK
    nombre = models.CharField(max_length=50)
    contacto = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    serie = models.CharField(max_length=15, primary_key=True)  # Serie como PK
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Almacen(models.Model):
    almacen_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Inventario(models.Model):
    inventario_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - {self.almacen.nombre}"
    
class Cliente(models.Model):
    dni = models.CharField(max_length=8, primary_key=True)  # DNI como PK
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Productividad(models.Model):
    productividad_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    horas_trabajadas = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion_actividad = models.TextField()

    def __str__(self):
        return f"{self.usuario.nombre} - {self.fecha}"
    
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_venta = models.DateField(auto_now_add=True)

    def total(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"Venta de {self.producto} a {self.cliente} el {self.fecha_venta}"