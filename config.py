import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (onde ficam as senhas e IDs)
load_dotenv()

# --- CONFIGURAÇÕES DO NÚCLEO ---

# O ano que o bot deve considerar para buscar os contratos e indicadores
YEAR = int(os.getenv("YEAR", 2026))

# O ID da Instância (Core) no sistema da BJ. 
# Exemplo: O Núcleo Campinas geralmente é 23. Cada núcleo/federação tem o seu.
# O ID da FEJESP é 5.
INSTANCE_ID = int(os.getenv("INSTANCE_ID", 5))

# Se "true", o bot só vai baixar contratos que já foram aprovados pela federação.
# Se "false", ele baixa tudo, inclusive os rascunhos.
ONLY_APPROVED = os.getenv("ONLY_APPROVED", "true").lower() == "true"

# O ID da sua planilha do Google Sheets (aquele código longo que fica na URL da planilha, entre "d/" e "/edit"). Exemplo: "1A2B3C4D5E6F7G8H9I0J"
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")