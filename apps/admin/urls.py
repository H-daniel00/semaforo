from django.urls import path
from .views import vPrinAdmin, vPrinUsuario, vPrinDireccion, vRegistroUsuarios, vRegistroDirecciones
app_name = 'admin'

urlpatterns = [
    path('', vPrinAdmin, name = 'prinAdmin'),
    #Usuarios
    path('usuarios', vPrinUsuario, name = 'prinUsuario'),
    path('usuario/agregar', vRegistroUsuarios, name = 'rUsuario'),
    #Direcciones
    path('direcciones', vPrinDireccion, name = 'prinDireccion'),
    path('direccion/agregar', vRegistroDirecciones, name = 'rDireccion'),
]