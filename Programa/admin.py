from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario,Categoria, Proveedor, Producto, Almacen, Inventario, Cliente, Productividad, Venta
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Formulario para agregar usuarios
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('dni', 'nombre', 'apellidos', 'correo', 'telefono', 'cargo', 'area', 'edad', 'foto', 'is_active', 'is_staff', 'is_admin')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Formulario para cambiar usuarios
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('dni', 'nombre', 'apellidos', 'correo', 'telefono', 'cargo', 'area', 'edad', 'foto', 'password', 'is_active', 'is_staff', 'is_admin', 'groups')

    def clean_password(self):
        return self.initial["password"]

# Definición del administrador personalizado para el modelo Usuario
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm  # Formulario de creación de usuario
    form = UserChangeForm  # Formulario de edición de usuario
    model = Usuario

    # Especifica qué campos mostrar en el panel de administración
    fieldsets = (
        (None, {'fields': ('dni', 'nombre', 'apellidos', 'correo', 'telefono', 'cargo', 'area', 'edad', 'foto', 'password', 'is_active', 'is_staff', 'is_admin', 'groups')}),
    )
    add_fieldsets = (
        (None, {'fields': ('dni', 'nombre', 'apellidos', 'correo', 'telefono','cargo', 'area', 'edad', 'foto', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin', 'groups')}),
    )

    # Especifica los campos para la visualización en el listado
    list_display = ('dni', 'nombre', 'apellidos', 'correo', 'telefono','cargo', 'area', 'edad', 'foto', 'is_active', 'is_staff', 'is_admin')
    ordering = ('dni',)

# Registra el modelo Usuario con el CustomUserAdmin
admin.site.register(Usuario, CustomUserAdmin)



# ACTUALIZA EN EL DASHBOARD DE DJANGO
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria_id', 'nombre')
    search_fields = ('nombre',)
    list_per_page = 25

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('ruc', 'nombre', 'contacto', 'telefono', 'correo')
    search_fields = ('nombre', 'ruc')
    list_per_page = 25

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('serie', 'nombre', 'precio', 'stock', 'categoria', 'proveedor')
    search_fields = ('nombre', 'serie')
    list_filter = ('categoria', 'proveedor')
    list_per_page = 25

class AlmacenAdmin(admin.ModelAdmin):
    list_display = ('almacen_id', 'nombre', 'direccion')
    search_fields = ('nombre',)
    list_per_page = 25

class InventarioAdmin(admin.ModelAdmin):
    list_display = ('inventario_id', 'producto', 'almacen', 'cantidad')
    search_fields = ('producto__nombre', 'almacen__nombre')
    list_per_page = 25

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellido', 'telefono', 'correo')
    search_fields = ('nombre', 'dni')
    list_per_page = 25

class ProductividadAdmin(admin.ModelAdmin):
    list_display = ('productividad_id', 'usuario', 'fecha', 'horas_trabajadas')
    search_fields = ('usuario__nombre',)
    list_filter = ('fecha',)
    list_per_page = 25
    
class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'producto', 'cantidad', 'fecha_venta', 'total')
    list_filter = ('fecha_venta',)

# Registro de los modelos en el administrador de Django con las configuraciones
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Productividad, ProductividadAdmin)
admin.site.register(Venta, VentaAdmin)