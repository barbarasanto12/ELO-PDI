from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Teste, Pergunta, Resposta, Resultado
from django.urls import reverse
from .models import Resposta
from .models import Pergunta, Resposta
from .models import Resultado
from aulas.models import AulaConcluida
from aulas.models import Aula, AulaConcluida
from testes.models import Teste
from utilizador.models import Utilizador
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from datetime import timedelta
from testes.models import Resultado
from aulas.models import Aula


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
    })

from .models import Teste

def pergunta_view(request, teste_id, pergunta_id):
    
    teste = get_object_or_404(Teste, id=teste_id)
    pergunta = get_object_or_404(Pergunta, id=pergunta_id, teste__id=teste_id)
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
    acertou = resposta.correta
    explicacao = resposta.explicacao

    # Gerenciar tentativas por pergunta usando sessão
    tentativas = request.session.get('tentativas', {})
    pergunta_id_str = str(pergunta.id)

    if pergunta_id_str not in tentativas:
        tentativas[pergunta_id_str] = 1
    else:
        if not acertou:
            tentativas[pergunta_id_str] += 1

    request.session['tentativas'] = tentativas

    if acertou:
        # Caso tenha acertado, vamos carregar a próxima pergunta
        proxima_pergunta = Pergunta.objects.filter(
            teste=pergunta.teste,
            id__gt=pergunta.id
        ).first()

        if proxima_pergunta:
            proxima_respostas = Resposta.objects.filter(pergunta=proxima_pergunta)
            return render(request, 'testes/resultado.html', {
                'acertou': True,
                'explicacao': explicacao,
                'proxima_pergunta': proxima_pergunta,
                'proxima_respostas': proxima_respostas,
            })
        else:
            # FIM DO TESTE: calcular pontuação
            total_perguntas = pergunta.teste.pergunta_set.count()
            pontuacao = 0

            # Considerar as tentativas feitas para cada pergunta
            for tentativas_feitas in tentativas.values():
                if tentativas_feitas == 1:
                    pontuacao += 1.0  # Pontuação total se acertou de primeira
                elif tentativas_feitas == 2:
                    pontuacao += 0.7  # Pontuação menor para segunda tentativa
                elif tentativas_feitas == 3:
                    pontuacao += 0.4  # Pontuação ainda menor para terceira tentativa
                else:
                    pontuacao += 0.2  # Pontuação mínima para outras tentativas

            # Calcular percentagem
            pontuacao_final = pontuacao  # pontuação em valor bruto (ex: 7.4)

            # Gravar o resultado
            Resultado.objects.create(
                teste=pergunta.teste,
                aluno=request.user,
                pontuacao=pontuacao_final,
                tentativas=sum(tentativas.values()),  # Soma total de tentativas
                tempo=timedelta(minutes=1)  # Ajustar para tempo real no futuro
            )

            # Limpar as tentativas da sessão
            if 'tentativas' in request.session:
                del request.session['tentativas']

            return redirect('testes:fim_teste', teste_id=pergunta.teste.id)

    else:
        # Resposta errada - Tentar novamente, mantendo a mesma pergunta
        return render(request, 'testes/resultado.html', {
            'acertou': False,
            'explicacao': explicacao,
            'pergunta': pergunta,  # Garantir que a mesma pergunta seja renderizada
        })



def fim_teste(request, teste_id):
    teste = get_object_or_404(Teste, id=teste_id)
    resultado = Resultado.objects.filter(teste=teste, aluno=request.user).first()

    if not resultado:
        return HttpResponse("Resultado não encontrado.")

    pontuacao = resultado.pontuacao
    total_perguntas = teste.pergunta_set.count()
    percentagem = round((pontuacao / total_perguntas) * 100, 2)

    aula_atual = teste.aula
    AulaConcluida.objects.get_or_create(user=request.user, aula=aula_atual)

    return render(request, 'testes/fim_teste.html', {
        'pontuacao': pontuacao,
        'total_perguntas': total_perguntas,
        'percentagem': percentagem,
        'aula_atual': aula_atual,
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
    resultados = Resultado.objects.filter(aluno=request.user)

    # Criar um dicionário com pontuação por teste
    pontuacoes_por_teste = {resultado.teste_id: resultado.pontuacao for resultado in resultados}

    # Prepara uma lista com dados extras
    testes_info = []
    for teste in testes:
        testes_info.append({
            'teste': teste,
            'pontuacao': pontuacoes_por_teste.get(teste.id),  # pode ser None se ainda não fez
            'perguntas_respondidas': Pergunta.objects.filter(teste=teste).count(),
        })

    return render(request, 'testes/lista_testes.html', {
        'testes_info': testes_info,
        'aulas_concluidas_ids': aulas_concluidas_ids,
    })
