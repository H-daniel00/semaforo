from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import fRegistroUsuarios
from apps.direccion.models import Usuarios, Permisos, Direcciones
from apps.direccion.forms import fRegistroDirecciones

@login_required
def vPrinAdmin(request):
    return render(request, 'admin/prinAdmin.html')

@login_required
def vPrinUsuario(request):
    fUsuario = fRegistroUsuarios()
    context = {'fUsuario': fUsuario}
    return render(request, 'admin/usuarios.html', context)

@login_required
def vPrinDireccion(request):
    fDireccion = fRegistroDirecciones()
    direcciones = Direcciones.objects.all()
    context = {'fDireccion': fDireccion, 'direcciones': direcciones}
    return render(request, 'admin/direcciones.html', context)

@login_required
def vRegistroUsuarios(request):
    if request.method == 'POST':
        fUsuario = fRegistroUsuarios(request.POST)
        if fUsuario.is_valid():
            usuario = fUsuario.save(commit = False)
            usuario.set_password(usuario.password)
            usuario.save()
    return redirect('admin:prinAdmin')

@login_required
def vRegistroDirecciones(request):
    if request.method == 'POST':
        fDireccion = fRegistroDirecciones(request.POST)
        if fDireccion.is_valid():
            fDireccion.save()
    return redirect('admin:prinAdmin')