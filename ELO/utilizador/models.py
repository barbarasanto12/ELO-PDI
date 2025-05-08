# utilizador/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilizador(AbstractUser):
    email = models.EmailField(unique=True)

    # Define o email como o campo usado para login
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']  # Campos obrigatórios na criação do utilizador

    def __str__(self):
        return self.email
from django.contrib.auth import get_user_model
User = get_user_model()

# models.py
class Aula(models.Model):
    ordem = models.IntegerField()
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return f"Aula {self.ordem} - {self.titulo}"


# utilizador/models.py
from django.db import models

