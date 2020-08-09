from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission, ContentType
from django.db.models import Q
from django import forms
import material

from gestao import models


class ModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome}"


class MultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome}"


class AssociadoCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.Associado
        fields = ('matricula', 'email',)


class AssociadoChangeForm(UserChangeForm):
    class Meta:
        model = models.Associado
        fields = ('matricula', 'email',)


class DiretorioAcademicoForm(forms.ModelForm):
    class Meta:
        model = models.DiretorioAcademico
        fields = ("nome", "sigla", "logo",)


class AreaForm(forms.ModelForm):
    class Meta:
        model = models.Area
        fields = ("nome", "gestor")


class DiretorCargoForm(forms.ModelForm):
    class Meta:
        model = models.Diretor
        fields = ("groups",)


class AssociadoForm(forms.ModelForm):
    layout = material.Layout(
        material.Fieldset("Informações Pessoais",
                          material.Row('nome', 'sobrenome'),
                          material.Row('email', 'telefone'),
                          ),
        material.Fieldset("Informações de Curso",
                          material.Row('matricula', 'ano_matricula', 'previsao_conclusao')
                          ),
    )

    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-telefone'}), required=False)

    class Meta:
        model = models.Associado
        fields = (
            "nome",
            "sobrenome",
            "matricula",
            "email",
            "ano_matricula",
            "previsao_conclusao",
            "telefone",
            "password",
        )


class AssociadoForm(forms.ModelForm):
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-telefone'}), required=False)
    layout = material.Layout(
        material.Fieldset("Informações Pessoais",
                          material.Row('nome', 'sobrenome'),
                          material.Row('email', 'telefone'),
                          ),
        material.Fieldset("Informações de Curso",
                          material.Row('matricula', 'ano_matricula', 'previsao_conclusao')
                          ),
    )

    class Meta:
        model = models.Diretor
        fields = ('nome', 'sobrenome', 'email', 'telefone', 'matricula', 'ano_matricula', 'previsao_conclusao')


class EgressoForm(forms.ModelForm):
    layout = material.Layout(
        material.Fieldset("Informações Pessoais",
                          material.Row('nome', 'sobrenome'),
                          material.Row('email', 'telefone'),
                          ),
        material.Fieldset("Informações de Curso",
                          material.Row('ano_matricula', 'previsao_conclusao')
                          ),
    )

    previsao_conclusao = forms.IntegerField(label="Ano de Conclusão", required=False)
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'mascara-telefone'}), required=False)

    class Meta:
        model = models.Egresso
        fields = (
            "nome",
            "sobrenome",
            "email",
            "ano_matricula",
            "previsao_conclusao",
            "telefone",
        )


class ReuniaoForm(forms.ModelForm):
    ata = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'editor'}))

    class Meta:
        model = models.Reuniao
        fields = ("data", "titulo", "ata", "presentes")


class GrupoForm(forms.ModelForm):
    layout = material.Layout(
        material.Row('name'),
        material.Fieldset('Permissões de Gestão',
                          material.Row(
                              material.Fieldset("Diretório Acadêmico",
                                                material.Column('change_diretorioacademico', 'view_diretorioacademico')
                                                ),
                              material.Fieldset("Atas de Reunião",
                                                material.Column('add_reuniao', 'change_reuniao', 'delete_reuniao',
                                                                'view_reuniao')
                                                ),
                              material.Fieldset("Áreas",
                                                material.Column('add_area', 'change_area', 'delete_area', 'view_area')
                                                ),
                          ),
                          material.Row(
                              material.Fieldset("Alunos",
                                                material.Column('add_aluno', 'change_aluno', 'delete_aluno',
                                                                'view_aluno')
                                                ),
                              material.Fieldset("Egressos",
                                                material.Column('add_egresso', 'change_egresso', 'delete_egresso',
                                                                'view_egresso')
                                                ),
                              material.Fieldset("Diretores",
                                                material.Column('add_diretor', 'change_diretor', 'delete_diretor',
                                                                'view_diretor')
                                                ),
                              material.Fieldset("Grupos",
                                                material.Column('add_group', 'change_group', 'delete_group',
                                                                'view_group')
                                                ),
                          ),
                          ),
        material.Fieldset('Permissões de Finanças',
                          material.Row(
                              material.Fieldset("Carteiras Financeiras",
                                                material.Column('add_carteira', 'change_carteira', 'delete_carteira',
                                                                'view_carteira')
                                                ),
                              material.Fieldset("Entradas Financeiras",
                                                material.Column('add_entradafinanceira', 'change_entradafinanceira',
                                                                'delete_entradafinanceira', 'view_entradafinanceira')
                                                ),
                              material.Fieldset("Saídas Financeiras",
                                                material.Column('add_saidafinanceira', 'change_saidafinanceira',
                                                                'delete_saidafinanceira', 'view_saidafinanceira')
                                                ),
                              material.Fieldset("Transferências Financeiras",
                                                material.Column('add_transferenciafinanceira',
                                                                'change_transferenciafinanceira',
                                                                'delete_transferenciafinanceira',
                                                                'view_transferenciafinanceira')
                                                ),
                          ),
                          material.Row(
                              material.Fieldset("Produtos",
                                                material.Column('add_produto', 'change_produto', 'delete_produto',
                                                                'view_produto')
                                                ),
                              material.Fieldset("Recibos de Pagamento",
                                                material.Column('add_recibopagamento', 'change_recibopagamento',
                                                                'delete_recibopagamento', 'view_recibopagamento')
                                                ),
                              material.Fieldset("Vendas",
                                                material.Column('add_venda', 'change_venda', 'delete_venda',
                                                                'view_venda')
                                                ),
                          ),
                          ),
        material.Fieldset('Permissões de Eventos',
                          material.Row(
                              material.Fieldset("Eventos",
                                                material.Column('add_evento', 'change_evento', 'delete_evento',
                                                                'view_evento')
                                                ),
                              material.Fieldset("Atrações de Eventos",
                                                material.Column('add_atracaoevento', 'change_atracaoevento',
                                                                'delete_atracaoevento', 'view_atracaoevento')
                                                ),
                              material.Fieldset("Inscrições de Eventos",
                                                material.Column('add_inscricaoevento', 'change_inscricaoevento',
                                                                'delete_inscricaoevento', 'view_inscricaoevento')
                                                ),
                              material.Fieldset("Inscrições em Atrações de Eventos",
                                                material.Column('add_inscricaoatracao', 'change_inscricaoatracao',
                                                                'delete_inscricaoatracao', 'view_inscricaoatracao')
                                                ),
                          ),
                          ),
    )

    __content_type_black_list = [
        'logentry',
        'permission',
        'content_type',
        'session',
        'cargo',
    ]

    __permission_black_list = [
        'add_diretorioacademico',
        'delete_diretorioacademico',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        permissions_add = Permission.objects.exclude(content_type__model__in=self.__content_type_black_list).exclude(
            codename__in=self.__permission_black_list).filter(codename__startswith='add_')
        permissions_change = Permission.objects.exclude(content_type__model__in=self.__content_type_black_list).exclude(
            codename__in=self.__permission_black_list).filter(codename__startswith='change_')
        permissions_delete = Permission.objects.exclude(content_type__model__in=self.__content_type_black_list).exclude(
            codename__in=self.__permission_black_list).filter(codename__startswith='delete_')
        permissions_view = Permission.objects.exclude(content_type__model__in=self.__content_type_black_list).exclude(
            codename__in=self.__permission_black_list).filter(codename__startswith='view_')

        for permission in permissions_add:
            self.fields[permission.codename] = forms.BooleanField(required=False, initial=False, label='Adicionar')

        for permission in permissions_change:
            self.fields[permission.codename] = forms.BooleanField(required=False, initial=False, label='Alterar')

        for permission in permissions_delete:
            self.fields[permission.codename] = forms.BooleanField(required=False, initial=False, label='Remover')

        for permission in permissions_view:
            self.fields[permission.codename] = forms.BooleanField(required=False, initial=False, label='Visualizar')

        if self.instance.id:
            group_permissions = self.instance.permissions.all()
            for permission in group_permissions:
                self.fields[permission.codename].initial = True

    def clean(self):
        data = {}
        data['name'] = self.cleaned_data.pop('name')
        data['permissions'] = []
        for permissao in self.cleaned_data:
            if self.cleaned_data[permissao]:
                data['permissions'].append(Permission.objects.get(codename=permissao))

        self.cleaned_data = data

    def save(self):
        group = super().save()
        group.permissions.clear()
        for permissao in self.cleaned_data['permissions']:
            group.permissions.add(permissao)

        return group

    class Meta:
        model = Group
        fields = ("name",)


class LinkCadastroForm(forms.ModelForm):
    class Meta:
        model = models.LinkCadastro
        fields = ('validade', 'tipo_usuario')
