from django.urls import path
from .views import vPrinAdmin, vRegistroUsuarios, vRegistroDirecciones
app_name = 'admin'

urlpatterns = [
    path('', vPrinAdmin, name = 'prinAdmin'),
    path('usuario/agregar', vRegistroUsuarios, name = 'rUsuario'),
    path('direccion/agregar', vRegistroDirecciones, name = 'rDireccion'),
]