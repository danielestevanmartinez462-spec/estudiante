
from django.db import models
from django.contrib.auth.models import User


# MODELO DE APRENDICES
class aprendiz(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='datos_aprendiz'
    )

    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    documento = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, unique=True)
    tipo_de_documento = models.CharField(max_length=25)

    ficha = models.ForeignKey(
        'programa',
        on_delete=models.CASCADE,
        related_name='aprendices',
        null=True,
        blank=True,
    )

    competencias = models.ManyToManyField(
        'competencias',
        related_name='aprendices',
        blank=True,
    )

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.documento}'


# MODELO DE PROGRAMAS
class programa(models.Model):
    nombre = models.CharField(max_length=30)
    ficha = models.IntegerField(unique=True)
    jornada = models.CharField(max_length=15)
    lugar = models.CharField(max_length=20)
    duracion = models.CharField(max_length=30)
    modalidad = models.CharField(max_length=15)
    nivel_de_profecion = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre} - Ficha {self.ficha}'


# MODELO DE INSTRUCTORES
class instructor(models.Model):
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    especialidad = models.CharField(max_length=25)
    documento = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.especialidad}'


# MODELO DE COMPETENCIAS
class competencias(models.Model):
    nombre = models.CharField(max_length=30)

    instructor = models.ForeignKey(
        'instructor',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nombre


# MODELO DE PERFILES Y ROLES
class Perfil(models.Model):

    ROLES = [
        ('ADMIN', 'Administrador'),
        ('INSTRUCTOR', 'Instructor'),
        ('APRENDIZ', 'Estudiante'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    rol_principal = models.CharField(
        max_length=20,
        choices=ROLES,
        default='APRENDIZ'
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return f'{self.usuario.username} - {self.get_rol_principal_display()}'
