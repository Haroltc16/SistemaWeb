from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import Venta

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="DNI", max_length=8)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Este usuario está inactivo.", code='inactive')


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'producto', 'cantidad']