# seu_app/models.py (substitua 'seu_app' pelo nome real do seu aplicativo Django)

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import uuid
from cloudinary.models import CloudinaryField

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

class Prato(models.Model):
    nome_prato = models.CharField(max_length=100)
    ingredientes = models.TextField()
    modo_preparo = models.CharField()
    tempo_preparo = models.IntegerField()
    rendimento = models.CharField(max_length=30, null=True)
    categoria = models.CharField(max_length=100, null=True)
    date_prato = models.DateTimeField(default=datetime.now, blank=True)
    funcionario = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    foto_prato = CloudinaryField(
        'foto_do_prato', 
        folder='canesgril_pratos', #NOME DA PASTA DENTRO DO CLOUDINARY
        #upload_to=get_file_path, # Para gerar o nome do arquivo
        blank=True,
        null=True
    )
    def __str__(self):
        return self.nome_prato

    '''
    class Meta:
        verbose_name = 'Prato'
        verbose_name_plural = 'Pratos'
    '''