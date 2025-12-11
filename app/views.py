from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Avg, Max, Min, Q, Prefetch
from django.views.defaults import page_not_found
from django.contrib import messages

from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required

# Create your views here.

def index(request):
    if(not 'fecha_inicio' in request.session):
        request.session['fecha_inicio'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render(request, 'index.html')

def borrar_session(request):
    del request.session['fecha_inicio']
    return render(request, 'index.html')

def registrar_usuario(request):
    if request.method == "POST":

                
            login(request, user)
            return redirect('index')
    else:
        return redirect( 'index')
    
    return render(request, 'registration/signup.html', {''}) 
    







#   PÁGINAS DE ERRORES
def mi_error_404(request, exception=None):
    return render(request, 'Errores/404.html',None,None,404)

def mi_error_400(request, exception=None):
    return render(request, 'Errores/400.html',None,None,400)

def mi_error_403(request, exception=None):
    return render(request, 'Errores/403.html',None,None,403)

def mi_error_500(request, exception=None):
    return render(request, 'Errores/500.html',None,None,500)