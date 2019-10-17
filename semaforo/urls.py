from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.direccion.views import vLogin, vLogout, vRegistroUsuarios


urlpatterns = [
    path('', vLogin, name = 'login'),
    path('direccion/', include('apps.direccion.urls', namespace = 'direccion')),
    path('admin/', include('apps.admin.urls', namespace = 'admin')),
    path('logout/', vLogout, name = 'logout'),
    path('registro/', vRegistroUsuarios, name = 'rUsuario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
