from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .models import Aula, Feedback
from django.contrib.auth.decorators import login_required
from testes.models import Teste  

@login_required
def ver_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    categorias_feedback = ["simplicidade", "interatividade", "clareza", "planeamento"]

    imagens_com_letras = []
    for i, imagem in enumerate(aula.imagens.all()):
        letra = chr(65 + i)  
        imagens_com_letras.append({
            'letra': letra,
            'imagem': imagem
        })

    teste = Teste.objects.filter(aula=aula).first()


    if teste:
        primeira_pergunta = teste.pergunta_set.order_by('numero').first()
        primeira_pergunta_numero = primeira_pergunta.numero if primeira_pergunta else None
    else:
        primeira_pergunta_numero = None

    return render(request, 'aulas/ver_aula.html', {
        'aula': aula,
        'categorias_feedback': categorias_feedback,
        'imagens_com_letras': imagens_com_letras,
        'teste': teste,
        'primeira_pergunta_numero': primeira_pergunta_numero,  
    })


@login_required
@require_POST
def submit_feedback(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    try:
        fb = Feedback.objects.create(
            aula           = aula,
            user           = request.user,
            simplicidade   = int(request.POST['simplicidade']),
            interatividade = int(request.POST['interatividade']),
            clareza        = int(request.POST['clareza']),
            planeamento    = int(request.POST['planeamento']),
        )
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Dados de feedback inválidos")
    return JsonResponse({'status': 'ok', 'message': 'Obrigado pelo teu feedback!'})

def lista_aulas(request):
    return render(request, 'aulas/ver_aula.html')