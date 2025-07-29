from supabase import create_client, Client
import os
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

# Substitua pelos seus dados
# É altamente recomendável definir estas variáveis de ambiente ANTES de executar o script
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") # Use sua service_role key para teste
BUCKET_NAME = os.environ.get("SUPABASE_BUCKET_NAME")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Erro: SUPABASE_URL ou SUPABASE_KEY não estão definidas como variáveis de ambiente.")
    print("Por favor, defina-as antes de executar o script. Exemplo:")
    print("export SUPABASE_URL=\"https://your-project-ref.supabase.co\"")
    print("export SUPABASE_KEY=\"eyJhbGciOiJIUzI1NiI...\"")
    exit(1)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Erro ao criar cliente Supabase: {e}")
    exit(1)

def create_dummy_image(filename="test_image.jpg"):
    try:
        img = Image.new("RGB", (100, 100), color = "red")
        img.save(filename)
        print(f"Arquivo de imagem dummy \'{filename}\' criado com sucesso.")
    except ImportError:
        print("Aviso: A biblioteca Pillow (PIL) não está instalada. Não foi possível criar a imagem dummy.")
        print("Por favor, crie manualmente um arquivo \'test_image.jpg\' no diretório atual.")
    except Exception as e:
        print(f"Erro ao criar imagem dummy: {e}")

def upload_test_file():
    file_path = "test_image.jpg"
    destination_path = "test_uploads/test_image.jpg" # Caminho dentro do bucket

    if not os.path.exists(file_path):
        print(f"Erro: Arquivo \'{file_path}\' não encontrado. Por favor, crie-o ou verifique o caminho.")
        return

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        print(f"Tentando fazer upload de \'{file_path}\' para \'{BUCKET_NAME}/{destination_path}\'...")
        res = supabase.storage.from_(BUCKET_NAME).upload(destination_path, data)
        print(f"Upload bem-sucedido: {res}")
        print(f"Verifique o Supabase Storage em: {SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{destination_path}")
    except Exception as e:
        print(f"Upload falhou: {e}")
        print("Possíveis causas: Políticas de RLS, chave de API incorreta, nome do bucket errado, ou problema de rede.")

if __name__ == "__main__":
    create_dummy_image()
    upload_test_file()
