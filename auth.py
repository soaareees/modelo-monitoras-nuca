import os
import requests
from dotenv import load_dotenv

# Carrega as senhas do arquivo .env
load_dotenv()

# Endereço base da API da Brasil Júnior
BASE_URL = "https://api.brasiljunior.org.br"

def get_token():
    """
    Esta função faz o 'login' no sistema da BJ usando o CPF e Senha
    e retorna um 'token' (uma chave digital) que permite buscar os dados.
    """
    
    # Busca as informações que o usuário preencheu no arquivo .env
    cpf = os.getenv("CPF")
    password = os.getenv("PASSWORD")

    # Endereço específico para pedir a chave de acesso (token)
    url = f"{BASE_URL}/oauth/token"

    # Dados que o bot envia para o sistema da BJ para provar quem ele é
    payload = {
        "login": cpf,
        "password": password,
        "grant_type": "password"
    }

    # Envia o pedido de login
    response = requests.post(url, data=payload)
    
    # Se o CPF ou Senha estiverem errados, o código vai parar aqui e avisar o erro
    response.raise_for_status()

    # Se der tudo certo, ele extrai a 'chave' (access_token) da resposta
    return response.json()["access_token"]