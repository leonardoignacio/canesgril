
from django.shortcuts import redirect, render, get_object_or_404
from .models import Prato
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    #lista_pratos = Prato.objects.all()
    lista_pratos = Prato.objects.order_by('date_prato').filter(publicado=True)
    paginator = Paginator(lista_pratos, 12) 
    page = request.GET.get('page')
    pratos_por_pagina = paginator.get_page(page) 
    return render(request, 'index.html', {'lista_pratos':pratos_por_pagina })

def churrasco(request, id):
    prato = get_object_or_404(Prato, id=id)
    return render(request, 'churrasco.html', {'prato': prato})

def buscar(request):
    nome_a_buscar = request.GET.get('buscar', '').strip()

    # Inicializa o queryset como vazio
    lista_pratos = Prato.objects.none()

    # Só realiza busca se algo foi digitado
    if nome_a_buscar:
        lista_pratos = Prato.objects.filter(
            publicado=True,
            nome_prato__icontains=nome_a_buscar
        ).order_by('date_prato')

    # Paginação mesmo se a busca não retornar nada
    paginator = Paginator(lista_pratos, 3)
    page = request.GET.get('page')
    pratos_por_pagina = paginator.get_page(page)

    return render(request, 'index.html', {
        'lista_pratos': pratos_por_pagina,
        'buscar': nome_a_buscar
    })
