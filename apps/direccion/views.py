from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , authenticate, logout
from django.contrib import messages
from .models import Usuarios, Actividades, Objetivos, Direcciones, getPercentActivity, getLightActivity
from .forms import fRegistroUsuariosDir

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

#---Actividades
@login_required
def vRegistroActividades(request):
    if request.method == 'POST':
        nombre = request.POST.get('act-name')
        direccion = request.POST.get('direccion', None)
        objs = request.POST.getlist('obj-name')
        objs_check = request.POST.getlist('obj-check')
        try:
            if direccion is None:
                direccion = request.user.direccion
            else:
                direccion = Direcciones.objects.get(id__exact = direccion)
            activity = Actividades.objects.create(nombre = nombre, direccion = direccion, usuario = request.user)
            for obj, checked in zip(objs, objs_check):
                if len(obj) > 0:
                    Objetivos.objects.create(nombre = obj, is_done = trueOrFalse(checked), actividad = activity)
            messages.success(request, 'Actividad agregada exitosamente')
        except:
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


@login_required
def vEliminarActividades(request, id):
    if request.method == 'GET':
        act = get_object_or_404(Actividades, pk = id)
        act.delete()
        messages.success(request, 'Actividad eliminada exitosamente')
    return redirect('direccion:prinDirect')

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

#Extra functions
def trueOrFalse(text):
    if text == 'true' or text == 'True':
        return True
    return False







