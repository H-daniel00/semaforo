from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.direccion.views import vPrincipal


urlpatterns = [
    path('direccion/', include('apps.direccion.urls', namespace = 'direccion')),
    path('admin/', include('apps.admin.urls', namespace = 'admin')),
    path('', vPrincipal, name = 'principal'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
