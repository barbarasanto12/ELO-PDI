from django.db import models
from aulas.models import Aula  # Importar apenas modelos necessários de outras apps



class Palavra(models.Model):
    texto = models.CharField(max_length=100)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)  # Relaciona com Aula
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)
    imagem = models.ImageField(upload_to='imagens_palavras/', null=True, blank=True)
    video = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.texto


class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo
