from django.urls import path
from .views import (
    vPrinAdmin, vPrinUsuario, vPrinDireccion, vRegistroUsuarios, vRegistroDirecciones, vEliminarDireccion,
    vCambiarContrasena, vEliminarUsuario, vResetDireccion, vEditarDireccion
)
app_name = 'admin'

urlpatterns = [
    path('', vPrinAdmin, name = 'prinAdmin'),
    #Usuarios
    path('usuarios', vPrinUsuario, name = 'prinUsuario'),
    path('usuario/agregar', vRegistroUsuarios, name = 'rUsuario'),
    path('usuario/<int:id>/cambiarcontra', vCambiarContrasena, name = 'cambiarPass'),
    path('usuario/<int:id>/eliminar', vEliminarUsuario, name = 'eUsuario'),
    #Direcciones
    path('direcciones', vPrinDireccion, name = 'prinDireccion'),
    path('direccion/agregar', vRegistroDirecciones, name = 'rDireccion'),
    path('direccion/<int:id>/editar', vEditarDireccion, name = 'edDireccion'),
    path('direccion/<int:id>/eliminar', vEliminarDireccion, name = 'eDireccion'),
    path('direccion/<int:id>/reset', vResetDireccion, name = 'resetDireccion'),
]