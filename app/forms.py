from django import forms
from django.forms import ModelForm
from .models import *
from .forms import *
from datetime import date


from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):
    ROLES = (
        ("", "Seleccione un rol"),
        (Usuario.INVESTIGADOR, "Investigador"),
        (Usuario.PACIENTE, "Paciente"),
    )
    edad = forms.IntegerField(required=False, label = 'Edad (solo para pacientes)', validators=[MinValueValidator(0), MaxValueValidator(120)])
    rol = forms.ChoiceField(choices=ROLES, label='Rol')
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'password1', 'password2']
    
    def clean(self):
        super().clean()
        
        rol = self.cleaned_data.get('rol')
        edad = self.cleaned_data.get('edad')
        if (rol == str(Usuario.PACIENTE))and( edad is None or edad == '' or edad < 0 or edad > 120):
            self.add_error('edad', 'La edad es obligatoria para el rol de paciente.')
            
        return self.cleaned_data


class EnsayoForm(ModelForm):
    class Meta:
        model = EnsayoClinico
        fields = ['nombre', 'descripcion', 'farmaco', 'pacientes', 'nivel_seguimiento', 'fecha_inicio', 'fecha_fin', 'activo']
        
        widgets = {
            'pacientes': forms.CheckboxSelectMultiple(),
            "fecha_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        farmaco = self.cleaned_data.get('farmaco')
        pacientes = self.cleaned_data.get('pacientes')
        nivel_seguimiento = self.cleaned_data.get('nivel_seguimiento')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        
        miNombre = EnsayoClinico.objects.filter(nombre=nombre).first()
        if (not (miNombre is None or (not self.instance is None and miNombre.id == self.instance.id ))):    
            self.add_error('nombre', 'El nombre del ensayo clínico ya existe. Debe ser único.')
        
        if descripcion is None or len(descripcion) < 100:
            self.add_error('descripcion', 'La descripción debe tener al menos 100 caracteres.')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio >= fecha_fin:
                self.add_error('fecha_inicio', 'La fecha de inicio debe ser anterior a la fecha de fin.')
                self.add_error('fecha_fin', 'La fecha de fin debe ser posterior a la fecha de inicio.')
            if fecha_fin < date.today():
                self.add_error('fecha_fin', 'La fecha de fin debe ser igual o posterior a la fecha actual.')



class FarmacoForm(ModelForm):
    class Meta:
        model = Farmaco
        fields = '__all__'
        
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        
        miNombre = Farmaco.objects.filter(nombre=nombre).first()
        if (not (miNombre is None or (not self.instance is None and miNombre.id == self.instance.id ))):    
            self.add_error('nombre', 'El nombre del fármaco ya existe. Debe ser único.')