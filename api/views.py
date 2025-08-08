from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from django.contrib.auth.models import User
from django.utils.dateformat import format
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

# Importe seu modelo Prato e o CloudinaryField
from churras.models import Prato


# --- Autenticação ---

@api_view(['POST'])
@permission_classes([AllowAny])
def py_cadastro(request):
    """
    Função para cadastrar um novo usuário.
    Espera um JSON com 'username', 'email', 'password' e 'password2'.
    Retorna um status de sucesso ou erro.
    """
    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    password2 = data.get('password2')

    if not all([username, email, password, password2]):
        return Response({'error': 'Todos os campos são obrigatórios: username, email, password e password2.'}, status=400)

    if password != password2:
        return Response({'error': 'As senhas não coincidem.'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Usuário já existe.'}, status=409)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    return Response({'status': 'success', 'message': 'Usuário criado com sucesso.'}, status=201)


# --- Funções CRUD de Pratos (atualizadas) ---

def _serialize_prato(prato):
    """Função auxiliar para serializar um objeto Prato para JSON."""
    return {
        'id': prato.id,
        'nome_prato': prato.nome_prato,
        'ingredientes': prato.ingredientes,
        'modo_preparo': prato.modo_preparo,
        'tempo_preparo': prato.tempo_preparo,
        'rendimento': prato.rendimento,
        'categoria': prato.categoria,
        'date_prato': format(prato.date_prato, 'Y-m-d H:i:s'),
        'funcionario_id': prato.funcionario.id if prato.funcionario else None,
        'publicado': prato.publicado,
        'foto_prato_url': prato.foto_prato.url if prato.foto_prato else None
    }


@api_view(['GET'])
@permission_classes([AllowAny])
def py_obter_pratos(request, prato_id=None):
    """
    Função para obter pratos.
    - Se `prato_id` for fornecido: retorna um prato específico.
    - Se `prato_id` for None: retorna todos os pratos.
    """
    if prato_id:
        try:
            prato = Prato.objects.get(pk=prato_id)
            prato_data = _serialize_prato(prato)
            return Response({'prato': prato_data})
        except Prato.DoesNotExist:
            return Response({'error': 'Prato não encontrado.'}, status=404)
    else:
        pratos = Prato.objects.all()
        pratos_data = [_serialize_prato(prato) for prato in pratos]
        return Response({'pratos': pratos_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def py_dashboard(request):
    """
    Função para listar os pratos do usuário logado.
    """
    pratos_do_usuario = Prato.objects.filter(funcionario=request.user)
    pratos_data = [_serialize_prato(prato) for prato in pratos_do_usuario]
    return Response({'pratos': pratos_data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def py_cria_prato(request):
    """
    Função para criar um novo prato.
    Espera um JSON com 'nome_prato', 'ingredientes', 'modo_preparo',
    'tempo_preparo', 'rendimento', 'categoria', e 'publicado'.
    """
    data = request.data
    prato = Prato.objects.create(
        nome_prato=data.get('nome_prato'),
        ingredientes=data.get('ingredientes'),
        modo_preparo=data.get('modo_preparo'),
        tempo_preparo=data.get('tempo_preparo'),
        rendimento=data.get('rendimento'),
        categoria=data.get('categoria'),
        publicado=data.get('publicado', False),
        funcionario=request.user # Associa o prato ao usuário logado
    )
    return Response({'status': 'success', 'prato_id': prato.id}, status=201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def py_deleta_prato(request, prato_id):
    """
    Função para deletar um prato específico.
    O usuário só pode deletar seus próprios pratos.
    """
    prato = get_object_or_404(Prato, pk=prato_id, funcionario=request.user)
    prato.delete()
    return Response({'status': 'success', 'message': f'Prato com ID {prato_id} deletado com sucesso.'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def py_edita_prato(request, prato_id):
    """
    Função para editar um prato específico.
    Espera um JSON com os campos a serem atualizados.
    O usuário só pode editar seus próprios pratos.
    """
    prato = get_object_or_404(Prato, pk=prato_id, funcionario=request.user)
    data = request.data
    
    # Atualiza apenas os campos presentes no JSON
    prato.nome_prato = data.get('nome_prato', prato.nome_prato)
    prato.ingredientes = data.get('ingredientes', prato.ingredientes)
    prato.modo_preparo = data.get('modo_preparo', prato.modo_preparo)
    prato.tempo_preparo = data.get('tempo_preparo', prato.tempo_preparo)
    prato.rendimento = data.get('rendimento', prato.rendimento)
    prato.categoria = data.get('categoria', prato.categoria)
    prato.publicado = data.get('publicado', prato.publicado)
    
    prato.save()
    return Response({'status': 'success', 'message': f'Prato com ID {prato_id} atualizado com sucesso.'})
