import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.db.models import Count
from .models import Usuarios, Actividades, Objetivos, Direcciones, Evidencias, getPercentActivity, getLightActivity
from .forms import fRegistroUsuariosDir
from .validate_file import validate_file_type, validate_img_type

def vLogin(request):
    if request.user.is_authenticated:
	    return redirect('direccion:logout')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        autenticar = authenticate(username = username, password = password)
        if autenticar is not None:
            auth_login(request, autenticar)
            if request.user.is_superuser :
                return redirect('admin:prinAdmin')
            elif request.user.direccion is not None:
                return redirect('direccion:prinDirect')
        else:
            messages.add_message(request, messages.ERROR,'Usuario y/o contraseña no válidos')
        return redirect('direccion:login')
    return render(request, 'base/login.html')

def vLogout(request):
    logout(request)
    return redirect('direccion:login')

@login_required
def vPrinDirec(request):
    return render(request, 'direccion/prinDirec.html')

def vPrincipal(request):
    context = {'direcciones': Direcciones.objects.exclude(codename = 'sg') }
    return render(request, 'base/main.html', context)

@login_required
def vPerfil(request):
    return render(request, 'direccion/perfil.html')

def vRegistroUsuarios(request):
    if request.method == 'POST':
        fUsuario = fRegistroUsuariosDir(request.POST, request.FILES)
        if fUsuario.is_valid():
            try:
                usuario = fUsuario.save(commit = False)
                pass_unhash = usuario.password
                usuario.set_password(usuario.password)
                usuario.save()
                usuario.direccion.titular = usuario
                usuario.direccion.save()
            except expression as identifier:
                print(identifier)
                messages.error(request,'Ha ocurrido un error. Intente de nuevo por favor')
                return redirect('direccion:rUsuario')    
            autenticar = authenticate(username = usuario.username, password = pass_unhash)
            if autenticar is not None:
                auth_login(request, autenticar)
                if request.user.direccion is not None:
                    return redirect('direccion:prinDirect')
                    messages.success(request, 'Registro con éxito - Bienvenido(a)')
                else:
                    print('ide1')
                    messages.error(request,'Ha ocurrido un error. Intente de nuevo por favor')
                    return redirect('direccion:login')
            else:
                print('ide2')
                messages.error(request,'Usuario y/o contraseña no válidos')
                return redirect('direccion:login')
        else:
            print('ide3')
            messages.error(request,'Ha ocurrido un error. Intente de nuevo por favor')
            return redirect('direccion:rUsuario')
    else:
        fUsuario = fRegistroUsuariosDir()
        context = {'fUsuario' : fUsuario}
    return render(request, 'base/registro.html', context)

# Verificar estas funciones
@login_required
def vCambiarAvatar(request):
    if request.method == 'POST': 
        usuario = request.user
        avatar = request.FILES.get('avatar')
        if avatar is not None:
            if validate_img_type(avatar):
                if usuario.avatar:
                    old_avatar = usuario.avatar.path
                    usuario.avatar = avatar
                    usuario.save()
                    try:
                        deleteFile(old_avatar)
                        messages.success(request, 'Avatar cambiado exitosamente')
                    except:
                        messages.error(request, 'Ha ocurrido un error, intente de nuevo')
                else:
                    usuario.avatar = avatar
                    usuario.save()
                    messages.success(request, 'Avatar cambiado exitosamente')
            else:
                messages.warning(request, 'Imagen inválida')
        else:
            messages.warning(request, 'Debe agregar una imagen')
    else:
        messages.error(request, 'Ha ocurrido un error, intente de nuevo')
    return redirect('direccion:perfil')

@login_required
def vCambiarNombreUsuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('name')
        apellido = request.POST.get('last_name')
        usuario = request.user
        if len(nombre) > 0:
            usuario.first_name = nombre
            usuario.last_name = apellido
            usuario.save()
            messages.success(request, 'Nombre cambiado exitosamente')
        else:
            messages.error(request, 'Debe de ingresar su nombre al menos')
    else:
        messages.error(request, 'Ha ocurrido un error, intente de nuevo')
    return redirect('direccion:perfil')

@login_required
def vCambiarPassword(request):
    if request.method == 'POST':
        current_pass = request.POST.get('current_pass')
        new_pass = request.POST.get('new_pass')
        if request.user.check_password(current_pass):
            request.user.set_password(new_pass)
            request.user.save(update_fields=['password'])
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Contraseña cambiada exitosamente')
        else:
            messages.warning(request, 'La contraseña no coincide con la actual. Intente de nuevo')
            return redirect('direccion:perfil')
    else:
        messages.error(request, 'Ha ocurrido un error inesperado')
    return redirect('direccion:login')

#---Actividades
@login_required
def vRegistroActividades(request):
    if request.method == 'POST':
        nombre = request.POST.get('act-name')
        direccion = request.POST.get('direccion', None)
        objs = request.POST.getlist('obj-name')
        objs_check = request.POST.getlist('obj-check')
        evidencias = request.FILES.getlist('evidencias')
        folio = 'ACT-'
        try:
            if direccion is None:
                direccion = request.user.direccion
            else:
                direccion = Direcciones.objects.get(id__exact = direccion)
            activity = Actividades.objects.create(nombre = nombre, direccion = direccion, usuario = request.user)
            activity.folio = folio + str(activity.id)
            activity.save()
            for obj, checked in zip(objs, objs_check):
                if len(obj) > 0:
                    pass
                    Objetivos.objects.create(nombre = obj, is_done = trueOrFalse(checked), actividad = activity)
            for evidencia in evidencias:
                Evidencias.objects.create(evidencia = evidencia, nombre = evidencia.name, actividad = activity)
            messages.success(request, 'Actividad agregada exitosamente')
        except Exception as e:
            print(e)
            messages.error(request, 'Ha ocurrido un error, inténtelo de nuevo')
    return redirect('direccion:prinDirect')

def vEditarActividad(request, id):
    if request.is_ajax():
        nombre = request.POST.get('new_name')
        try:
            act = Actividades.objects.get(id = id)
            act.nombre = nombre
            act.save()
            info = {
                'status' : 'success',
                'text' : 'Actividad actualizada exitosamente'
            }
        except:
            info = {
                'status' : 'error',
                'text' : 'Al parecer algo salió mal. Intente de nuevo'
            }
    else:
        info = {
            'status' : 'error',
            'text' : 'Al parecer algo salió mal. Intente de nuevo'
        }    
    return JsonResponse(info, safe = False)

def vEditarComentario(request, id):
    if request.is_ajax():
        comentario = request.POST.get('comment')
        try:
            act = Actividades.objects.get(id = id)
            act.comentarios = comentario
            act.save()
            info = {
                'status' : 'success',
                'text' : 'Cambios guardados exitosamente'
            }
        except:
            info = {
                'status' : 'error',
                'text' : 'Al parecer algo salió mal. Intente de nuevo'
            }
    else:
        info = {
            'status' : 'error',
            'text' : 'Al parecer algo salió mal. Intente de nuevo'
        }    
    return JsonResponse(info, safe = False)

@login_required
def vEliminarActividades(request, id):
    if request.method == 'GET':
        act = get_object_or_404(Actividades, pk = id)
        act.delete()
        messages.success(request, 'Actividad eliminada exitosamente')
    return redirect('direccion:prinDirect')

def vObtenerActividades(request):
    if request.is_ajax():
        direcciones = Direcciones.objects.exclude(see_in_list = False).order_by('nombre')
        data_dir = []
        for direccion in direcciones:
            data_dir.append({
                'name': direccion.nombre,
                'titular': getTitularName(direccion),
                'avatar': getAvatarUrl(direccion),
                'activities': getJsonAct(direccion.actividades.all())
            })
        print(data_dir)
        return  JsonResponse(data_dir, safe = False)
    else:
        return HttpResponse('maaaaall no lo soy')

def getAvatarUrl(direction):
    try:
        return direction.titular.avatar.url
    except Exception as identifier:
        return None

def getTitularName(direction):
    try:
        return direction.titular.get_full_name()
    except Exception as identifier:
        return 'No asignado'

def getJsonAct(activities):
    data = []
    if len(activities) > 0:
        for act in activities:
            data.append({
                'name': act.nombre,
                'percent': act.get_porcent(),
                'color': act.get_light()
            })
    else:
        data = None
    return data

#---Objetivos
@login_required
def vEliminarObjetivo(request, id):
    if request.method == 'GET':
        try:
            obj = Objetivos.objects.get(id = id)
            obj.delete()
            messages.success(request, 'Objetivo eliminado exitosamente')
        except:
            messages.error(request, 'Ha ocurrido un error, inténtelo de nuevo')
    else:
        messages.error(request, 'Ha ocurrido un error, inténtelo de nuevo')
    return redirect('direccion:prinDirect')

def vEditarObjetivo(request, id):
    if request.is_ajax():
        nombre = request.POST.get('new_name')
        try:
            obj = Objetivos.objects.get(id = id)
            obj.nombre = nombre
            obj.save()
            info = {
                'status' : 'success',
                'text' : 'Objetivo actualizado exitosamente'
            }
        except:
            info = {
                'status' : 'error',
                'text' : 'Al parecer algo salió mal. Intente de nuevo'
            }
    else:
        info = {
            'status' : 'error',
            'text' : 'Al parecer algo salió mal. Intente de nuevo'
        }    
    return JsonResponse(info, safe = False)

def vAgregarObjetivos(request):
    if request.is_ajax():
        obj_name = request.POST.get('obj_name')
        obj_check = request.POST.get('obj_check')
        act_id = request.POST.get('act_id')
        try:
            act = Actividades.objects.get(id__exact = act_id)
            obj = Objetivos.objects.create(nombre = obj_name, is_done = trueOrFalse(obj_check), actividad = act)
            info = {
                'status' : 'success',
                'text' : 'Objetivo agregado exitosamente',
                'obj_value': obj.id,
                'percent' : obj.actividad.get_porcent(),
                'color' : obj.actividad.get_light(),
                'delete_url' : redirect('direccion:eObjetivo', id = obj.id).url, 
                'edit_url' : redirect('direccion:edObjetivo', id = obj.id).url
            }
        except Exception as identifier:
            print(identifier)
            info = {
                'status' : 'error',
                'text' : 'Al parecer algo salió mal. Intente de nuevo'
            }
    else:
        info = {
            'status' : 'error',
            'text' : 'Al parecer algo salió mal. Intente de nuevo'
        }
    return JsonResponse(info, safe = False)


@login_required
def vEditarCheckObjetivo(request):
    if request.is_ajax():
        id_obj = request.POST.get('id')
        check_status = request.POST.get('status_check')
        try:
            obj = Objetivos.objects.get(pk = id_obj)
            obj.is_done = trueOrFalse(check_status)
            obj.save()       
            info = {
                'status' : 'success',
                'text' : 'Cambios guardados exitosamente',
                'percent' : obj.actividad.get_porcent(),
                'color' : obj.actividad.get_light()
            }
        except:
            info = {
                'status' : 'error',
                'text' : 'Al parecer algo salió mal. Intente de nuevo'
            }
    else:
        info = {
            'status' : 'error',
            'text' : 'Al parecer algo salió mal. Intente de nuevo'
            }          
    return JsonResponse(info, safe = False)

#---Evidencias
def vAgregarEvidencias(request):
    if request.method == 'POST':
        msj = ''
        evidencias = request.FILES.getlist('evidencias')
        id_act = request.POST.get('actividad')
        try:
            actividad = Actividades.objects.get(id = id_act)
            for evidencia in evidencias:
                if validate_file_type(evidencia):
                    if evidencia.size <= 5242880:
                        Evidencias.objects.create(evidencia = evidencia, nombre = evidencia.name, actividad = actividad)
                        msj += ("<h6 class='right-align green-text'>" + evidencia.name + " se guardó correctamente" + "</h6>") 
                    else:
                        msj += ("<h6 class='right-align red-text'>" +evidencia.name + " excede peso permitido" + "</h6>")
                else:
                    msj += ("<h6 class='right-align red-text'>" +evidencia.name + " archivo inválido" + "</h6>")
            messages.info(request, msj)
            return redirect('direccion:prinDirect')
        except Exception as identifier:
            print(identifier)
            messages.error(request, 'Al parecer algo salió mal. Intente de nuevo')
            return redirect('direccion:prinDirect')
    else:
        messages.error(request, 'Al parecer algo salió mal. Intente de nuevo')
        return redirect('direccion:prinDirect')

def vEliminarEvidencias(request, id):
    if request.method == 'GET':
        try:
            evidencia = Evidencias.objects.get(id = id)
            deleteFile(evidencia.evidencia.path)
            evidencia.delete()
            messages.success(request, 'Evidencia eliminada existosamente')
            return redirect('direccion:prinDirect')
        except Exception as identifier:
            print(identifier)
            messages.error(request, 'Al parecer algo salió mal. Intente de nuevo')
            return redirect('direccion:prinDirect')
    else:
        messages.error(request, 'Al parecer algo salió mal. Intente de nuevo')
        return redirect('direccion:prinDirect')
        
#Extra functions
def trueOrFalse(text):
    if text == 'true' or text == 'True':
        return True
    return False

def deleteFile(path):
    if os.path.isfile(path):
        os.remove(path)






