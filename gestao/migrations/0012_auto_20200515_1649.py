# Generated by Django 3.0.6 on 2020-05-15 16:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0011_auto_20200507_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('gestao.associado',),
        ),
        migrations.CreateModel(
            name='Diretor',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('gestao.associado',),
        ),
        migrations.CreateModel(
            name='Egresso',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('gestao.associado',),
        ),
        migrations.AlterField(
            model_name='reuniao',
            name='presentes',
            field=models.ManyToManyField(blank=True, related_name='reunioes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Cargo',
        ),
    ]