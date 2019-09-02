from django.urls import path
from .views import (vLogin, vLogout, vPrinDirec, 
                    vRegistroActividades, vEliminarActividades, vEditarActividad, 
                    vEditarCheckObjetivo, vEliminarObjetivo, vEditarObjetivo, 
                    vRegistroUsuarios)
app_name = 'direccion'

urlpatterns = [
    path('', vPrinDirec, name = 'prinDirect'),
    path('acceso/', vLogin, name = "login"),
    path('logout/', vLogout, name = 'logout'),
    path('registro/', vRegistroUsuarios, name = 'rUsuario'),
    #Activities
    path('actividad/agregar', vRegistroActividades, name = 'rActividad'),
    path('actividad/<int:id>/eliminar', vEliminarActividades, name = 'eActividad'),
    #Objetivos
    path('actividad/objetivo/<int:id>/eliminar', vEliminarObjetivo, name = 'eObjetivo'),
    #Ajax
    path('ajax/actividad/objetivo/editarcheck', vEditarCheckObjetivo),
    path('ajax/actividad/<int:id>/editar', vEditarActividad, name = 'edActividad'),
    path('ajax/actividad/objetivo/<int:id>/editar', vEditarObjetivo, name = 'edObjetivo'),
]