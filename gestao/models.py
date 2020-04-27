from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import AssociadoManager

class Area(models.Model):
    nome = models.CharField(max_length=50)

class Associado(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=60)
    ano_matricula = models.DateField(null=True)
    previsao_conclusao = models.DateField(null=True)
    telefone = models.CharField(max_length=30, null=True)
    matricula = models.CharField(max_length=30, unique=True)
    foto = models.FileField(null=True)
    usuario_externo = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'matricula'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']

    objects = AssociadoManager()

class Gestor(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    ano_gestao = models.IntegerField()
    associado = models.OneToOneField(Associado, on_delete=models.PROTECT, primary_key=True)

class Reuniao(models.Model):
    data = models.DateField(auto_now=True)
    ata = models.TextField()
    presentes = models.ManyToManyField(Associado)

class DiretorioAcademico(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.FileField(null=True)

