from django.shortcuts import render, get_object_or_404
from aulas.models import Aula, Imagem, Palavra, AulaConcluida, Video 
from django.db.models import Q
def pesquisa_view(request):
    query = request.GET.get('q', '')
    user = request.user

    resultados_aulas = []
    resultados_imagens = []
    resultados_videos = []
    resultados_palavras = []
    aulas_concluidas = []

    if user.is_authenticated:
       
        aulas_concluidas = Aula.objects.filter(
            id__in=AulaConcluida.objects.filter(user=user).values_list('aula_id', flat=True)
        ).order_by('ordem')

        if query:
            
            resultados_aulas = aulas_concluidas.filter(
                Q(titulo__icontains=query) | Q(descricao__icontains=query)
            ).distinct()

           
            resultados_imagens = Imagem.objects.filter(
                aula__in=aulas_concluidas,
                descricao__icontains=query
            )

           
            resultados_videos = Video.objects.filter(
                aula__in=aulas_concluidas,
                descricao__icontains=query
            )

           
            resultados_palavras = Palavra.objects.filter(
                texto__icontains=query
            )

    context = {
        'query': query,
        'aulas_concluidas': aulas_concluidas,
        'resultados_aulas': resultados_aulas,
        'resultados_imagens': resultados_imagens,
        'resultados_videos': resultados_videos,
        'resultados_palavras': resultados_palavras,
    }

    return render(request, 'pesquisa/resultados.html', context)

def detalhes_aula_view(request, aula_id):
    user = request.user
    aula = get_object_or_404(Aula, id=aula_id)

   
    if not AulaConcluida.objects.filter(user=user, aula=aula).exists():
        return render(request, 'pesquisa/nao_autorizado.html', status=403)

    imagens = aula.imagens.all()
    videos = aula.videos.all()

    return render(request, 'pesquisa/detalhes_aula.html', {
        'aula': aula,
        'imagens': imagens,
        'videos': videos
    })


