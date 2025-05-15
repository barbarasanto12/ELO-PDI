from django.contrib import admin
from .models import Palavra, Categoria

@admin.register(Palavra)
class PalavraAdmin(admin.ModelAdmin):
    list_display = ('texto', 'aula', 'categoria')  
    search_fields = ('texto',)  
    list_filter = ('aula', 'categoria')  

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao')  
    search_fields = ('titulo',)  
