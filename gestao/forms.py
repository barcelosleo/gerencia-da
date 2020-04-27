from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import Associado, DiretorioAcademico


class AssociadoCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Associado
        fields = ('matricula', 'email',)


class AssociadoChangeForm(UserChangeForm):

    class Meta:
        model = Associado
        fields = ('matricula', 'email',)

class DiretorioAcademicoForm(ModelForm):
    class Meta:
        model = DiretorioAcademico
        fields = ("nome", "logo",)

