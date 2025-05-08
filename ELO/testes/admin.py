from django.contrib import admin
from .models import Pergunta, Teste, Resposta, Resultado

from django.utils.html import format_html

class RespostaInline(admin.StackedInline):
    model = Resposta
    fields = ('imagem', 'video', 'preview_midia', 'texto', 'correta')  
    readonly_fields = ('preview_midia',)              
    extra = 4

    def preview_midia(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="max-height:120px;" />', obj.imagem.url)
        elif obj.video:
            return format_html(
                '<video controls style="width:150px !important; height:auto !important; display:block;">'
                '<source src="{}" type="video/mp4">'
                'Seu navegador não suporta vídeo.'
                '</video>',
                obj.video.url
            )
        return "(sem mídia)"
    preview_midia.short_description = 'Pré‑visualização'


class PerguntaInline(admin.TabularInline):
    model = Pergunta
    extra = 1
    fields = ['teste', 'texto']
    
class TesteAdmin(admin.ModelAdmin):
    inlines = [PerguntaInline]
list_display = ('titulo', 'aula') 
fields = ('titulo', 'aula', 'mensagem_inicial','total_perguntas','perguntas_respondidas')



def estado_display(self, obj):
      return obj.estado
estado_display.short_description = 'Estado'


class PerguntaAdmin(admin.ModelAdmin):
    inlines = [RespostaInline]
    list_display = ('texto', 'teste') 


admin.site.register(Teste, TesteAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Resposta)  # Opcional, mas útil para debug
admin.site.register(Resultado)
