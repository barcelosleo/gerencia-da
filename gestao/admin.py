from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AssociadoCreationForm, AssociadoChangeForm
from .models import Associado, Area


class AssociadoAdmin(UserAdmin):
    add_form = AssociadoCreationForm
    form = AssociadoChangeForm
    model = Associado
    list_display = ('email', 'nome', 'is_staff', 'is_active',)
    list_filter = ('email', 'nome', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('matricula', 'password')}),
        ('Personal info', {'fields': ('nome', 'sobrenome', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricula', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('matricula', 'nome', 'sobrenome', 'email')
    ordering = ('matricula', 'nome', 'sobrenome', 'email')
    filter_horizontal = ('groups', 'user_permissions',)

class AreaAdmin(admin.ModelAdmin):
    fields = ('nome',)
    list_display = ('nome',)



admin.site.register(Associado, AssociadoAdmin)
admin.site.register(Area, AreaAdmin)

