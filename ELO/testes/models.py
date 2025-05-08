# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.conf import settings

class Teste(models.Model):
    titulo = models.CharField(max_length=200)
    aula = models.ForeignKey('aulas.Aula', on_delete=models.CASCADE)
    mensagem_inicial = models.TextField(blank=True, null=True)

def __str__(self):
        return self.titulo
@property
def total_perguntas(self):
        return self.pergunta_set.count()
 


class Pergunta(models.Model):
    TESTE_TIPO_CHOICES = [
        ('imagem', 'Imagem'),
        ('video', 'Vídeo'),
    ]

    teste = models.ForeignKey(Teste, on_delete=models.CASCADE)
    texto = models.TextField()
    tipo = models.CharField(max_length=10, choices=TESTE_TIPO_CHOICES, default='imagem')
    video = models.FileField(upload_to='videos_perguntas/', blank=True, null=True)  # Só se for tipo vídeo
    imagem = models.ImageField(upload_to='perguntas/', blank=True, null=True)  # Só se for tipo imagem

    def __str__(self):
        return self.texto

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='respostas/', blank=True, null=True)  # Imagem opcional
    video = models.FileField(upload_to='videos_respostas/', blank=True, null=True)  # Novo campo de v
    correta = models.BooleanField(default=False)
    explicacao = models.TextField(blank=True, null=True)
    texto = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):  
        return self.texto or f"Imagem: {self.imagem or self.video}"

class Resultado(models.Model):
    teste = models.ForeignKey(Teste, on_delete=models.CASCADE)
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pontuacao = models.FloatField(default=0)
    tentativas = models.IntegerField(default=0)  # Número total de tentativas
    tempo = models.DurationField(default=timedelta)
    data_realizacao = models.DateTimeField(auto_now_add=True)

class Aula(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
    
#class Teste(models.Model):
 #
 #    titulo = models.CharField(max_length=200)
   # mensagem_inicial = models.TextField(blank=True, null=True)  # novo campo

    #def __str__(self):
     #   return self.titulo

    #@property
    #def total_perguntas(self):
     #   return self.pergunta_set.count()