import os
import io
import zipfile
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from .models import Actividades, Evidencias

def descargarEvidenciasZip(request, id):
    try:
        activity = Actividades.objects.get(id__exact = id)
        if activity.evidencias.count() > 0:
            return makeZip(activity.evidencias.all(), activity.nombre)
        else:
            return HttpResponse('No se encontraron evidencias')
    except Exception as identifier:
        print(identifier)
        messages.success(request, 'Ha ocurrido un error. Intente de nuevo')
        return redirect('direccion:prinDirect')
             
def makeZip(files, zipName):
    # En caso de querer meterlo en una subcarpeta los archivos
    # Por el momento, solo crea el nombre del zip
    zip_name = 'Evidencias - ' + zipName 
    zip_filename = "%s.zip" % zip_name
    # String IO para guardar en memoria el zip 
    s = io.BytesIO()
    # El compresor
    zf = zipfile.ZipFile(s,"w")
    for fpath in files:
        path2 = fpath.evidencia.path
        fdir, fname = os.path.split(path2)
        print(fdir, fname)
        zip_path = os.path.join(zip_name, fname)
        zf.write(path2, zip_path)
    zf.close()
     # Tomamos el zip de la memoria y realizamos el response
    resp = HttpResponse(s.getvalue(), content_type="application/application/octet-stream")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return resp


