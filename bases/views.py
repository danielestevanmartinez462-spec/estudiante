from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from .forms import AprendizForm
from .models import aprendiz


# LOGIN SEGUN EL ROL

class LoginPorRolView(LoginView):
    template_name = 'bases/login.html'

    def form_valid(self, form):
        rol_seleccionado = self.request.POST.get('rol')
        usuario = form.get_user()

        if usuario.is_superuser:
            rol_real = 'ADMIN'
        else:
            perfil = getattr(usuario, 'perfil', None)
            rol_real = perfil.rol_principal if perfil else None

        if rol_seleccionado != rol_real:
            form.add_error(
                None,
                'El tipo de usuario seleccionado no corresponde a tu cuenta.'
            )
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        destino = self.get_redirect_url()

        if destino:
            return destino

        return reverse('listar_aprendices')


# COMPROBAR PERMISOS
def roles_requeridos(*roles):
    def decorador(vista):
        @wraps(vista)
        @login_required(login_url='login')
        def verificar(request, *args, **kwargs):

            if request.user.is_superuser:
                return vista(request, *args, **kwargs)

            perfil = getattr(request.user, 'perfil', None)

            if perfil and perfil.rol_principal in roles:
                return vista(request, *args, **kwargs)

            raise PermissionDenied

        return verificar
    return decorador



# LISTADO DE APRENDICES
@login_required(login_url='login')
def listar_aprendices(request):

    if request.user.is_superuser:
        rol_usuario = 'ADMIN'
        aprendices = aprendiz.objects.all()

    else:
        perfil = getattr(request.user, 'perfil', None)

        if perfil is None:
            raise PermissionDenied

        rol_usuario = perfil.rol_principal

        if rol_usuario == 'APRENDIZ':
            aprendices = aprendiz.objects.filter(usuario=request.user)

        elif rol_usuario in ['ADMIN', 'INSTRUCTOR']:
            aprendices = aprendiz.objects.all()

        else:
            raise PermissionDenied

    return render(request, 'bases/lista_aprendiz.html', {
        'aprendices': aprendices,
        'rol_usuario': rol_usuario
    })


# CREAR APRENDIZ
@roles_requeridos('ADMIN', 'INSTRUCTOR')
def crear_aprendiz(request):

    if request.method == 'POST':
        form = AprendizForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Aprendiz registrado correctamente.')
            return redirect('listar_aprendices')
    else:
        form = AprendizForm()

    return render(request, 'bases/crear_aprendiz.html', {
        'form': form
    })


# EDITAR APRENDIZ
@roles_requeridos('ADMIN', 'INSTRUCTOR')
def editar_aprendiz(request, documento):

    aprendiz_obj = get_object_or_404(aprendiz, documento=documento)

    if request.method == 'POST':
        form = AprendizForm(request.POST, instance=aprendiz_obj)
    else:
        form = AprendizForm(instance=aprendiz_obj)

    form.fields['documento'].disabled = True

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Se editó de manera correcta')
        return redirect('listar_aprendices')

    return render(request, 'bases/crear_aprendiz.html', {
        'form': form,
        'titulo': f'Editar {aprendiz_obj.nombre} - {aprendiz_obj.apellido}',
    })


# ELIMINAR APRENDIZ
@roles_requeridos('ADMIN', 'INSTRUCTOR')
def eliminar_aprendiz(request, documento):

    aprendiz_obj = get_object_or_404(aprendiz, documento=documento)

    if request.method == 'POST':
        aprendiz_obj.delete()
        messages.success(request, 'Se eliminó el aprendiz correctamente')
        return redirect('listar_aprendices')

    return render(request, 'bases/eliminar_aprendiz.html', {
        'aprendiz_objs': aprendiz_obj
    })


# BUSCAR APRENDIZ
@roles_requeridos('ADMIN', 'INSTRUCTOR')
def buscar_aprendiz(request):

    resultado = None

    if request.method == 'POST':
        documento = request.POST.get('documento', '').strip()
        resultado = aprendiz.objects.filter(documento=documento).first()

        if resultado is None:
            messages.error(
                request,
                f'No se encontró ningún aprendiz con el documento {documento}.'
            )

    return render(request, 'bases/buscar.html', {
        'aprendiz': resultado
    })


# MAPA
@roles_requeridos('ADMIN', 'INSTRUCTOR')
def mapa(request):
    return render(request, 'bases/mapa.html')
