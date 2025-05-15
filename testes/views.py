from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Teste, Pergunta, Resposta, Resultado, TentativaPergunta
from django.urls import reverse
from aulas.models import Aula, AulaConcluida
from testes.models import Teste, Resultado
from utilizador.models import Utilizador
from datetime import timedelta
from django.utils import timezone




@login_required
def realizar_teste(request, teste_id):
    teste = get_object_or_404(Teste, id=teste_id)
    perguntas = Pergunta.objects.filter(teste=teste)

    if request.method == 'POST':
        respostas_usuario = request.POST
        pontuacao = 0

        
        for pergunta in perguntas:
            resposta_selecionada_id = respostas_usuario.get(f'pergunta_{pergunta.id}')
            if resposta_selecionada_id:
                try:
                    resposta = Resposta.objects.get(id=resposta_selecionada_id, pergunta=pergunta)
                    if resposta.correta:
                        pontuacao += 1
                except Resposta.DoesNotExist:
                    pass

       
        resultado = Resultado.objects.create(
            teste=teste,
            aluno=request.user,
            pontuacao=pontuacao
        )

       
        return redirect('fim_teste', teste_id=teste.id)

    return render(request, 'testes/teste.html', {'teste': teste, 'perguntas': perguntas})

def resultado_view(request, teste_id, pergunta_id, resposta_id):
    resposta = get_object_or_404(Resposta, id=resposta_id)
    acertou = resposta.correta
    pergunta = resposta.pergunta

    return render(request, 'testes/resultado.html', {
        'pergunta': pergunta,
        'acertou': acertou,
         'teste': teste_id,
    })

def pergunta_view(request, teste_id, pergunta_numero):
    teste = get_object_or_404(Teste, id=teste_id)
    pergunta = get_object_or_404(teste.pergunta_set.all(), numero=pergunta_numero)
    respostas = Resposta.objects.filter(pergunta=pergunta)

    return render(request, 'testes/perguntas.html', {
        'teste_id': teste_id,
        'pergunta': pergunta,
        'respostas': respostas,
        'teste': teste,
    })


def verificar_resposta_direta(request, resposta_id):
    resposta = get_object_or_404(Resposta, id=resposta_id)
    pergunta = resposta.pergunta
    teste = pergunta.teste

    tentativa, created = TentativaPergunta.objects.get_or_create(
        utilizador=request.user,
        pergunta=pergunta,
        teste=teste
    )

    if not tentativa.acertou:  
        tentativa.tentativas += 1
        tentativa.acertou = resposta.correta
        tentativa.save()

    if tentativa.acertou:
        
        proxima_pergunta = Pergunta.objects.filter(teste=teste, numero=pergunta.numero + 1).first()
        if proxima_pergunta:
            return redirect('testes:pergunta_view', teste_id=teste.id, pergunta_numero=proxima_pergunta.numero)
        else:
           
            return redirect('testes:fim_teste', teste_id=teste.id)
    else:
        return render(request, 'testes/resultado.html', {
            'pergunta': pergunta,
            'acertou': False,
            'explicacao': resposta.explicacao,
            'teste': teste,
        })

def fim_teste(request, teste_id):
    teste = get_object_or_404(Teste, id=teste_id)
    tentativas = TentativaPergunta.objects.filter(utilizador=request.user, teste=teste)

    total_perguntas = teste.pergunta_set.count()
    pontuacao = tentativas.filter(acertou=True, tentativas=1).count()  
    percentagem = round((pontuacao / total_perguntas) * 100, 2)

    resultado, created = Resultado.objects.get_or_create(
        teste=teste,
        aluno=request.user,
        defaults={
            'pontuacao': percentagem,
            'tentativas': tentativas.count(),
        }
    )
    if not created:
        resultado.pontuacao = percentagem
        resultado.tentativas = tentativas.count()
        resultado.save()

    AulaConcluida.objects.get_or_create(user=request.user, aula=teste.aula)

    return render(request, 'testes/fim_teste.html', {
        'pontuacao': pontuacao,
        'total_perguntas': total_perguntas,
        'percentagem': percentagem,
        'teste': teste,
    })



  
def progresso(request):
    
    resultados = Resultado.objects.filter(aluno=request.user).order_by('-data_realizacao')
    
    
    return render(request, 'utilizadores/progresso.html', {
        'resultados': resultados
    })

def lista_testes(request):
    testes = Teste.objects.all()
    aulas_concluidas_ids = AulaConcluida.objects.filter(user=request.user).values_list('aula_id', flat=True)

    testes_info = []
    for teste in testes:
        
        tentativas = TentativaPergunta.objects.filter(utilizador=request.user, teste=teste)
        
        acertos = tentativas.filter(acertou=True, tentativas=1).count()

        total_perguntas = teste.pergunta_set.count()  
        
        concluido = teste.aula.id in aulas_concluidas_ids

        testes_info.append({
            'teste': teste,
            'acertos': acertos,
            'total_perguntas': total_perguntas,
            'concluido': concluido,
        })

    return render(request, 'testes/lista_testes.html', {
        'testes_info': testes_info,
    })
