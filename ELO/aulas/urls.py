from django.urls import path
from . import views


urlpatterns = [
    
    path('aula/<int:aula_id>/', views.ver_aula, name='ver_aula'),
    path('aula/<int:pk>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('', views.lista_aulas, name='aulas'), 
    
    # Adicione mais rotas conforme necessário
]


   


