from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from gestao.models import (
    Associado,
    Aluno,
    Diretor,
    Egresso,
    Externo,
)


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(matricula='00203070', email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(matricula='00203070', email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('00203070', 'super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                matricula='00203070', email='super@user.com', password='foo', is_superuser=False)


class AssociadoTestCase(TestCase):
    def setUp(self):
        Associado.objects.create(
            nome="Some",
            sobrenome="User",
            matricula="00302060",
            email="some@user.com",
        )

    def test_nomesobrenome(self):
        some_user = Associado.objects.get(nome="Some")
        self.assertEqual(some_user.nome_completo, "Some User")


class GruposAssociadoTestCase(TestCase):
    def __cria_grupos(self):
        Group.objects.create(
            name="Diretor"
        )
        Group.objects.create(
            name="Aluno"
        )
        Group.objects.create(
            name="Egresso"
        )
        Group.objects.create(
            name="Usuário Externo"
        )

    def __cria_associados(self):
        Aluno.objects.create(
            nome="Aluno",
            sobrenome="Teste",
            matricula="00302061",
            email="s1@t.com"
        )
        Diretor.objects.create(
            nome="Diretor",
            sobrenome="Teste",
            matricula="00302062",
            email="s2@t.com"
        )
        Egresso.objects.create(
            nome="Egresso",
            sobrenome="Teste",
            matricula="00302063",
            email="s3@t.com"
        )
        Externo.objects.create(
            nome="Externo",
            sobrenome="Teste",
            matricula="00302064",
            email="s4@t.com"
        )

    def setUp(self):
        self.__cria_grupos()
        self.__cria_associados()

    def test_diretor(self):
        diretor = Diretor.objects.get(nome="Diretor")
        grupo = Group.objects.get(name="Diretor")

        self.assertTrue(grupo in diretor.groups.all())

    def test_aluno(self):
        aluno = Aluno.objects.get(nome="Aluno")
        grupo = Group.objects.get(name="Aluno")

        self.assertTrue(grupo in aluno.groups.all())

    def test_egresso(self):
        egresso = Egresso.objects.get(nome="Egresso")
        grupo = Group.objects.get(name="Egresso")

        self.assertTrue(grupo in egresso.groups.all())

    def test_externo(self):
        externo = Externo.objects.get(nome="Externo")
        grupo = Group.objects.get(name="Usuário Externo")

        self.assertTrue(grupo in externo.groups.all())
