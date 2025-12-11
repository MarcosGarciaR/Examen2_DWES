from django.urls import path, re_path
from .import views


urlpatterns = [
    path('', views.index , name='index'),
    path('registrar', views.registrar_usuario, name='registrar_usuario'),
    
]