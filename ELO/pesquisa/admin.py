# pesquisa/admin.py
from django.contrib import admin
from .models import Palavra, Categoria

@admin.register(Palavra)
class PalavraAdmin(admin.ModelAdmin):
    list_display = ('texto', 'aula', 'categoria')  # Campos a serem exibidos no admin
    search_fields = ('texto',)  # Permitir pesquisa por texto
    list_filter = ('aula', 'categoria')  # Filtros laterais no admin

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao')  # Campos a serem exibidos no admin
    search_fields = ('titulo',)  # Permitir pesquisa por título
