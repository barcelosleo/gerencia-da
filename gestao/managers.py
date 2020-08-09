from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
import random


def matricula_randomica(nome, sufixo):
    matricula = str(int(random.random() * 1e17))
    return sufixo + matricula + "".join(random.sample(nome.strip(), 3)).upper()


class AssociadoManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, matricula, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(matricula=matricula, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, matricula, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(matricula, email, password, **extra_fields)


class AlunoManager(models.Manager):
    def get_queryset(self):
        return super(AlunoManager, self).get_queryset().filter(is_staff=False)

    def create(self, **kwargs):
        kwargs.update({'is_staff': False})
        return super(AlunoManager, self).create(**kwargs)


class DiretorManager(models.Manager):
    def get_queryset(self):
        return super(DiretorManager, self).get_queryset().filter(is_staff=True)

    def create(self, **kwargs):
        kwargs.update({'is_staff': True})
        return super(DiretorManager, self).create(**kwargs)


class EgressoManager(models.Manager):
    def get_queryset(self):
        return super(EgressoManager, self).get_queryset().filter(is_active=False)

    def create(self, **kwargs):
        nome = kwargs.get('nome', '*!@')
        kwargs.update({
            'is_active': False,
            'matricula': matricula_randomica(nome, 'EGR')
        })
        return super(EgressoManager, self).create(**kwargs)


class ExternoManager(models.Manager):
    def get_queryset(self):
        return super(ExternoManager, self).get_queryset().filter(is_external=True)

    def create(self, **kwargs):
        nome = kwargs.get('nome', '*!@')
        kwargs.update({
            'is_external': True,
            'matricula': matricula_randomica(nome, 'EXT')
        })
        return super(ExternoManager, self).create(**kwargs)
