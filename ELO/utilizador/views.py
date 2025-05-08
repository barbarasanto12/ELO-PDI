from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
from aulas.models import Aula
from aulas.models import Aula, AulaConcluida

def home(request):
    return render(request, 'utilizador/home.html')

#def criar_conta(request):
 #   return render(request, 'utilizador/criar_conta.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
             login(request, user)
             return redirect('dashboard')
        else:
            messages.error(request, 'Credenciais inválidas')
            return redirect('login')  # Redireciona de volta ao login em caso de erro
    return render(request, 'utilizador/login.html')

@login_required(login_url='login')

def dashboard(request):
    return render(request, 'utilizador/dashboard.html')

def password(request):
    return render(request, 'utilizador/password.html')

def quem_somos(request):
    return render(request, 'utilizador/quem_somos.html')

from django.shortcuts import render, redirect
from django.urls import reverse

def criar_conta_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usuário no banco de dados

            # Captura os dados necessários para o redirecionamento
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            # Redireciona para a página de login com os dados na query string
            login_url = f"{reverse('login')}?email={email}&password={password}"
            return redirect(login_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'utilizador/criar_conta.html', {'form': form})


from django.shortcuts import render
from aulas.models import Aula, AulaConcluida

def dashboard(request):
    aulas = Aula.objects.order_by('ordem')
    concluidas_ids = set(AulaConcluida.objects.filter(user=request.user).values_list('aula_id', flat=True))

    aulas_info = []
    desbloquear_proxima = True  # Começamos com a primeira aula desbloqueada

    for aula in aulas:
        if aula.id in concluidas_ids:
            estado = 'concluida'
        elif desbloquear_proxima:
            estado = 'desbloqueada'
            desbloquear_proxima = False  # Só desbloqueia a próxima ainda não concluída
        else:
            estado = 'bloqueada'

        aulas_info.append({
            'aula': aula,
            'estado': estado
        })

    return render(request, 'utilizador/dashboard.html', {'aulas_info': aulas_info})

from django.contrib.auth.views import PasswordResetView

from django.utils import translation
from django.contrib.auth.views import PasswordResetView

class CustomPasswordResetView(PasswordResetView):
    template_name = 'utilizador/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'

    def dispatch(self, *args, **kwargs):
        # Defina a linguagem como português antes de processar a solicitação
        translation.activate('pt-pt')  # Ativar português
        return super().dispatch(*args, **kwargs)
