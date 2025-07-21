import os
from django.conf import settings
import django
import sqlite3

# configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canesgril.settings')
django.setup()

# conecta diretamente ao arquivo db.sqlite3
conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
cur  = conn.cursor()

# lê e executa seu SQL em lote
with open('popula_pratos.sql', 'r', encoding='utf-8') as f:
    cur.executescript(f.read())

conn.commit()
conn.close()
print("20 pratos inseridos com sucesso!")
