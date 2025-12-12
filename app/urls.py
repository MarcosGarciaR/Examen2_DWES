from django.urls import path, re_path
from .import views


urlpatterns = [
    path('', views.index , name='index'),
    path('registrar', views.registrar_usuario, name='registrar_usuario'),
    
    path('ensayos/', views.ver_ensayos, name='ver_ensayos'),
    path('ensayos/crear/', views.crear_ensayo, name='crear_ensayo'),
    path('ensayo/editar/<int:ensayo_id>', views.ensayo_editar, name='editar_ensayo'),
    path('ensayo/eliminar/<int:ensayo_id>', views.ensayo_eliminar, name='eliminar_ensayo'),
    
    path('crearfarmaco/', views.crear_farmaco, name='crear_farmaco'),
    path('farmacos/', views.ver_farmacos, name='ver_farmacos'),
]