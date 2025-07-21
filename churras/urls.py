from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('<int:id>', churrasco, name='churrasco'),
    path('buscar/', buscar, name='buscar')
]
