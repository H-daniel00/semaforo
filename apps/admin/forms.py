from django import forms
from apps.direccion.models import Usuarios

class fRegistroUsuarios(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['username', 'password', 'first_name', 'direccion']
        widgets = {
            'password' : forms.PasswordInput(render_value = True),
        }

class fCambiarContrasena(forms.Form):
    password = forms.CharField(label = 'Contraseña', max_length = 128, widget = forms.PasswordInput())
    repeat_password = forms.CharField(label = 'Confirme la contraseña', max_length = 128, widget = forms.PasswordInput())

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data['repeat_password']
        if not repeat_password == self.cleaned_data['password']:
            raise forms.ValidationError('La contraseña no coincide', code='invalid')
        return repeat_password