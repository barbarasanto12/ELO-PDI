from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilizador

class UtilizadorAdmin(UserAdmin):
    model = Utilizador
    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {'fields': ('idade', 'bio')}),
    )

admin.site.register(Utilizador, UtilizadorAdmin)
