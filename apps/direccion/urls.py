from django.urls import path
from .views import vLogin, vLogout, vPrinDirec, vRegistroActividades, vEliminarActividades, vEditarCheckObjetivo, vRegistroUsuarios
app_name = 'direccion'

urlpatterns = [
    path('', vPrinDirec, name = 'prinDirect'),
    path('acceso/', vLogin, name = "login"),
    path('logout/', vLogout, name = 'logout'),
    path('registro/', vRegistroUsuarios, name = 'rUsuario'),

    #Activities
    path('actividad/agregar', vRegistroActividades, name = 'rActividad'),
    path('actividad/<int:id>/eliminar', vEliminarActividades, name = 'eActividad'),

    #Ajax
    path('ajax/actividad/objetivo/editarcheck', vEditarCheckObjetivo),
]