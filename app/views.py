from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Avg, Max, Min, Q, Prefetch
from django.views.defaults import page_not_found
from django.contrib import messages

from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required

# Create your views here.

def ver_ensayos(request):
    ensayos = EnsayoClinico.objects.all()
    return render(request, 'URLs/ensayos/lista_ensayos.html', {'mostrar_ensayos': ensayos})

def crear_ensayo(request):
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = EnsayoForm(datosFormulario)
    
    if(request.method == "POST"):
        ensayo_creado = crear_ensayo_modelo(formulario)
        if(ensayo_creado):
            messages.success(request, "Se ha creado el ensayo con nombre "+str(formulario.cleaned_data.get('nombre'))+ " correctamente")
            return redirect("ver_ensayos")
                
    return render(request, 'URLs/ensayos/create.html', {'formulario':formulario})

def crear_ensayo_modelo(formulario):
    ensayo_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            ensayo_creado = True
        except Exception as error:
            print(error)
    
    return ensayo_creado



def ensayo_editar(request, ensayo_id):
    ensayo = EnsayoClinico.objects.get(id = ensayo_id)
    datosFormulario = None
    
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = EnsayoClinico(datosFormulario, instance = ensayo)
    
    
    if(request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado el ensayo '+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('ver_ensayos')
            except Exception as e:
                print(e)
    
    return render(request, 'URLs/ensayos/actualizar.html', {'formulario':formulario, 'ensayo':ensayo})


def ensayo_eliminar(request, ensayo_id):
    ensayo = EnsayoClinico.objects.get(id = ensayo_id)
    try:
        ensayo.delete()
    except Exception as e:
        print(e)
    
    return redirect('ver_ensayos')


def ver_farmacos(request):
    farmacos = Farmaco.objects.all()
    return render(request, 'URLs/farmacos/lista_farmacos.html', {'mostrar_farmacos': farmacos})

def crear_farmaco(request):
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = FarmacoForm(datosFormulario)
    
    if(request.method == "POST"):
        farmaco_creado = crear_farmaco_modelo(formulario)
        if(farmaco_creado):
            messages.success(request, "Se ha creado el farmaco con nombre "+str(formulario.cleaned_data.get('nombre'))+ " correctamente")
            return redirect("ver_farmacos")
                
    return render(request, 'URLs/farmacos/create.html', {'formulario':formulario})

def crear_farmaco_modelo(formulario):
    farmaco_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            farmaco_creado = True
        except Exception as error:
            print(error)
    
    return farmaco_creado




def index(request):
    if(not 'fecha_inicio' in request.session):
        request.session['fecha_inicio'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render(request, 'index.html')

def borrar_session(request):
    del request.session['fecha_inicio']
    return render(request, 'index.html')

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
            
        if form.is_valid():
            user = form.save()
            rol = int(form.cleaned_data.get('rol'))
            
            if rol == Usuario.INVESTIGADOR:
                grupo = Group.objects.get(name='Investigadores')
                grupo.user_set.add(user)
                investigador = Investigador.objects.create(usuario=user)
                investigador.save()
                
            elif rol == Usuario.PACIENTE:
                edad = form.cleaned_data.get('edad')
                grupo = Group.objects.get(name='Pacientes')
                grupo.user_set.add(user)
                Paciente.objects.create(usuario=user,edad=edad)
                
            login(request, user)
            return redirect('index')
    else:
        form = RegistroForm()
    
    return render(request, 'registration/signup.html', {'formRegistro': form}) 
    







#   PÁGINAS DE ERRORES
def mi_error_404(request, exception=None):
    return render(request, 'Errores/404.html',None,None,404)

def mi_error_400(request, exception=None):
    return render(request, 'Errores/400.html',None,None,400)

def mi_error_403(request, exception=None):
    return render(request, 'Errores/403.html',None,None,403)

def mi_error_500(request, exception=None):
    return render(request, 'Errores/500.html',None,None,500)