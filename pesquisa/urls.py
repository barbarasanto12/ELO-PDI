from django.urls import path
from . import views

urlpatterns = [
    path('', views.pesquisa_view, name='pesquisa'),
    path('aula/<int:aula_id>/', views.detalhes_aula_view, name='detalhes_aula'),
]


