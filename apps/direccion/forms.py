from django import forms
from .models import Usuarios, Direcciones

class fRegistroDirecciones(forms.ModelForm):
    class Meta:
        model = Direcciones
        fields = '__all__'

class fRegistroUsuariosDir(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['username', 'password', 'first_name', 'direccion', 'avatar']
        widgets = {
            'password' : forms.PasswordInput(render_value = True),
        }