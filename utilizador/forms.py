from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilizador

class CustomUserCreationForm(UserCreationForm):
  class Meta:
        model = Utilizador
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nome de Utilizador',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirmar Password',
        }


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilizador

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Utilizador
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nome de Utilizador',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirmar Password',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Utilizador.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
