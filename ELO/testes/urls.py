from django.urls import path
from . import views

app_name = 'testes'  

urlpatterns = [
    path('realizar_teste/<int:teste_id>/', views.realizar_teste, name='realizar_teste'),
    #path('perguntas/<int:teste_id>/<int:pergunta_id>/', views.pergunta_view, name='perguntas'),
    path('verificar_resposta/<int:resposta_id>/', views.verificar_resposta_direta, name='verificar_resposta'),
    path('perguntas/<int:id>/', views.pergunta_view, name='pergunta'),
    
    path('fim_teste/<int:teste_id>/', views.fim_teste, name='fim_teste'),

    path('progresso/', views.progresso, name='progresso'),
    path('testes/perguntas/<int:teste_id>/<int:pergunta_id>/', views.pergunta_view, name='perguntas'),
    path('testes/', views.lista_testes, name='lista_testes'),
    
]

    
