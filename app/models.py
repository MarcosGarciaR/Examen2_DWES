from django.db import models
from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    RECEPCIONISTA = 2  
    CUIDADOR = 3
    CLIENTE = 4
    ROLES = (
        (ADMINISTRADOR , 'administrador'),
    (RECEPCIONISTA, 'recepcionista'),
    (CUIDADOR , 'cuidador'),
    (CLIENTE , 'cliente'),
    )

    rol = models.PositiveSmallIntegerField(
        choices = ROLES, default=1
    )
    