from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Aula(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    ordem = models.IntegerField(default=0)  
    numero = models.IntegerField()
    
    def __str__(self):
        return self.titulo
    
class Imagem(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='aulas/')
    descricao = models.TextField()

    def __str__(self):
        return f"Imagem de {self.aula.titulo}"
    
class Video(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    descricao = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Vídeo de {self.aula.titulo}"


class Feedback(models.Model):
    aula = models.ForeignKey(
        'Aula',
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    simplicidade    = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    interatividade  = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    clareza         = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    planeamento     = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    criado_em       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback #{self.pk} – Aula {self.aula.id}'
    
class AulaConcluida(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    data_conclusao = models.DateTimeField(auto_now_add=True) 
    class Meta:
        unique_together = ('user', 'aula')  # Evita duplicações

    def __str__(self):
        return f"{self.user} concluiu {self.aula}"

class Palavra(models.Model):
    texto = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='palavras/', null=True, blank=True)
    video = models.FileField(upload_to='palavras/videos/', null=True, blank=True)

    def __str__(self):
        return self.texto
