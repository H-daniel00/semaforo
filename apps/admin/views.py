from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import fRegistroUsuarios, fCambiarContrasena
from apps.direccion.models import Usuarios, Permisos, Direcciones
from apps.direccion.forms import fRegistroDirecciones

# check admin
def check_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    else:
        return False


@login_required
@user_passes_test(check_admin)
def vPrinAdmin(request):
    return render(request, 'admin/prinAdmin.html')

@login_required
@user_passes_test(check_admin)
def vPrinUsuario(request):
    fUsuario = fRegistroUsuarios()
    usuarios = Usuarios.objects.filter(is_active = True)
    context = {'fUsuario': fUsuario, 'usuarios': usuarios}
    return render(request, 'admin/usuarios.html', context)

@login_required
@user_passes_test(check_admin)
def vPrinDireccion(request):
    fDireccion = fRegistroDirecciones()
    direcciones = Direcciones.objects.order_by('is_active')
    context = {'fDireccion': fDireccion, 'direcciones': direcciones}
    return render(request, 'admin/direcciones.html', context)

@login_required
@user_passes_test(check_admin)
def vRegistroUsuarios(request):
    if request.method == 'POST':
        fUsuario = fRegistroUsuarios(request.POST)
        if fUsuario.is_valid():
            usuario = fUsuario.save(commit = False)
            usuario.set_password(usuario.password)
            usuario.save()
    return redirect('admin:prinAdmin')

@login_required
@user_passes_test(check_admin)
def vEliminarUsuario(request, id):
    try:
        usuario = Usuarios.objects.get(id = id)
        usuario.is_active = False
        usuario.save()
        messages.success(request, 'El usuario ha sido eliminado exitosamente')
        return redirect('admin:prinUsuario')
    except Usuarios.DoesNotExist:
        return redirect('admin:prinUsuario')

@login_required
@user_passes_test(check_admin)
def vCambiarContrasena(request, id):
    try:
        usuario = Usuarios.objects.get(id = id)
        if request.method == 'POST':
            fpass = fCambiarContrasena(request.POST)
            if fpass.is_valid():
                usuario.set_password(fpass.cleaned_data['password'])
                usuario.save()
                messages.success(request, 'La contraseña se cambió exitosamente')
                return redirect('admin:prinUsuario')
            else:
                messages.error(request, 'No se pudo actualizar la contraseña')
                return redirect('admin:cambiarPass', usuario.id)
        else:
            fpass = fCambiarContrasena(label_suffix = '')
        context = {'fpass': fpass, 'user_full_name': usuario.get_full_name()}
        return render(request, 'admin/reset_password.html', context)
    except Usuarios.DoesNotExist:
        return redirect('admin:prinUsuario')
        
@login_required
@user_passes_test(check_admin)
def vRegistroDirecciones(request):
    if request.method == 'POST':
        fDireccion = fRegistroDirecciones(request.POST)
        if fDireccion.is_valid():
            direccion = fDireccion.save(commit=False)
            direccion.is_active = True
            direccion.save()
    return redirect('admin:prinDireccion')

@login_required
@user_passes_test(check_admin)
def vEliminarDireccion(request, id):
    if request.method == 'GET':
        try:
            direccion = Direcciones.objects.get(id = id)
            direccion.is_active = False
            direccion.save()
            messages.success(request, 'Dirección deshabilitada exitosamente')
        except Exception as identifier:
            messages.error(request,'Ha ocurrido un error. Intente de nuevo por favor')
    else:
        messages.error(request,'Ha ocurrido un error. Intente de nuevo por favor')
    return redirect('admin:prinDireccion')

@login_required
@user_passes_test(check_admin)
def vResetDireccion(request, id):
    if request.method == 'GET':
        try:
            direccion = Direcciones.objects.get(id = id)
            for act in direccion.actividades.all():
                act.delete()
            messages.success(request, 'Dirección reiniciada exitosamente')
        except Direcciones.ObjectDoesNotExists:
            messages.error(request,'No existe esa dirección')
    else:
        messages.error(request,'Ha ocurrido un error. Intente de nuevo por favor')
    return redirect('admin:prinDireccion')