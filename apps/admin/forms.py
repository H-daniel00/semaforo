from django import forms
from apps.direccion.models import Usuarios

class fRegistroUsuarios(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['username', 'password', 'first_name', 'direccion']
        widgets = {
            'password' : forms.PasswordInput(render_value = True),
        }