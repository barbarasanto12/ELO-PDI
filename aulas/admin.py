from django.contrib import admin
from .models import Aula, Imagem, Feedback
from django.contrib import admin
from .models import AulaConcluida 
from .models import Aula, Imagem, Video


class ImagemInline(admin.TabularInline):
    model = Imagem
    extra = 1  

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    
class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0
    readonly_fields = ('user', 'simplicidade', 'interatividade',
                       'clareza', 'planeamento', 'criado_em')
    can_delete = False

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    inlines = [ImagemInline, FeedbackInline,VideoInline] 
    list_display = ('titulo', 'ordem')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('aula', 'user', 'simplicidade', 'interatividade',
                    'clareza', 'planeamento', 'criado_em')
    list_filter = ('aula', 'criado_em')
    search_fields = ('user__username',)


class AulaConcluidaAdmin(admin.ModelAdmin):
    list_display = ('user', 'aula', 'data_conclusao')  
    search_fields = ('user__username', 'aula__titulo')  
    list_filter = ('data_conclusao',)  

admin.site.register(AulaConcluida, AulaConcluidaAdmin)
