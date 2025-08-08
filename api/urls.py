from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

# O nome da app é importante para o namespace, evitando conflitos de nomes de rotas
app_name = 'api'

urlpatterns = [
    # Rotas de autenticação baseadas em token JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Rota para cadastro de usuário.
    path('cadastro', views.py_cadastro, name='cadastro'),
    
    # Rotas para listar todos os pratos ou obter um prato específico
    # Para obter todos os pratos, chame a rota sem o ID: /api/pratos/
    # Para obter um prato específico, chame com o ID: /api/pratos/1/
    path('pratos/', views.py_obter_pratos, name='obter_pratos'),
    path('pratos/<int:prato_id>', views.py_obter_pratos, name='obter_prato_detalhe'),

    # Rotas do dashboard (pratos do usuário autenticado)
    path('dashboard', views.py_dashboard, name='dashboard'),
    
    # Rotas para o CRUD de pratos
    path('cria-prato', views.py_cria_prato, name='cria_prato'),
    path('deleta/<int:prato_id>', views.py_deleta_prato, name='deleta_prato'),
    path('atualiza/<int:prato_id>', views.py_edita_prato, name='edita_prato'),
]