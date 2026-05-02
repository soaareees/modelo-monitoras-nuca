import sys
import os
import time

# Este bloco garante que o bot consiga encontrar todas as pastas internas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Importamos as ferramentas que configuramos
from src.auth import get_token
from src.api.client import BJClient
from src.services.contracts_service import ContractsService
from src.services.contracts_processor import ContractsProcessor
from src.services.sheets_service import SheetsService
from src.config import YEAR, INSTANCE_ID, ONLY_APPROVED, SPREADSHEET_ID

def main():
    """
    Função principal que coordena o bot: 
    Login -> Busca Contratos -> Busca Membros -> Salva no Sheets
    """
    # 1. Faz o login no sistema da Brasil Júnior
    token = get_token()

    # 2. Prepara o 'navegador' do bot com a chave de acesso
    client = BJClient(token)

    # --- 3. FLUXO DE CONTRATOS (Aba: Dados Brutos) ---
    print("Iniciando busca de contratos no Portal...")
    contracts_service = ContractsService(client)
    
    # Busca todos os contratos do ano e núcleo configurados
    contracts = contracts_service.get_contracts(
        instance_id=INSTANCE_ID,
        year=YEAR
    )

    processor = ContractsProcessor(only_approved=ONLY_APPROVED)
    
    # Prepara os dados para a planilha colocando o título das colunas na primeira linha
    contracts_rows = []
    contracts_rows.append(["ID", "EJ", "Mês", "# Soluções", "Faturamento", "Data", "É colaborativo", "Agente de mercado", "Fat Colab"])
    
    for i, c in enumerate(contracts, start=1):
        data = c.get_data()
        data[0] = i  # Gera um número sequencial (1, 2, 3...)
        contracts_rows.append(data)

    print(f"✅ {len(contracts_rows) - 1} contratos processados.")

    # --- 4. FLUXO DE INDICADORES (Aba: Dados Brutos - Indicadores) ---
    # Este bloco tenta pegar dados consolidados (pode falhar se o site da BJ estiver lento)
    print("\nColetando indicadores estratégicos...")
    indicator_endpoint = f"/portal/instances/cores/{INSTANCE_ID}/reports/network_growth"
    indicator_rows = [['ID', 'EJ', 'Cluster Atual', 'Cluster Previsto', 'Faturamento', 'CSAT Parcial', '% de ECM', 'Taxa Collab (%)']]

    try:
        response = client.get(indicator_endpoint, params={"year": YEAR})
        growth_data = response.get('record', {}).get('network_growth', {})
        
        for cluster_key in growth_data:
            for ej in growth_data[cluster_key].get('ejs', []):
                indicator_rows.append([
                    ej.get('id'), ej.get('name'), ej.get('this_year_cluster'),
                    ej.get('next_year_cluster'), ej.get('revenue'), ej.get('csat'),
                    ej.get('collaborative_members'), ej.get('collaborative_rate')
                ])
        print(f"✅ Indicadores coletados.")
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível carregar indicadores estratégicos (Erro: {e}).")

    # --- 5. FLUXO DE MEMBROS (Aba: Dados Brutos - Membros) ---
    # Aqui o bot pergunta EJ por EJ quantas pessoas existem em cada cargo
    print("\nColetando detalhamento de membros por EJ...")
    
    # Extraímos a lista de IDs de EJs que vieram no fluxo de indicadores para o loop
    # Se o fluxo anterior falhou, você pode definir uma lista manual de IDs aqui.
    EJS_PARA_CENSO = [row[0] for row in indicator_rows[1:]] if len(indicator_rows) > 1 else []
    
    member_rows = [['ID', 'EJ', 'Membros com Pendência', 'Administradores', 'Diretores', 'Membros', 'Trainees']]

    for i, ej_id in enumerate(EJS_PARA_CENSO, start=1):
        try:
            print(f"[{i}/{len(EJS_PARA_CENSO)}] Coletando dados da EJ {ej_id}...", end="\r")
            ej_res = client.get(f"/portal/ejs/{ej_id}")
            ej_data = ej_res.get('record', {})

            member_rows.append([
                ej_id,
                ej_data.get('name'),
                ej_data.get('invalid_members_size', 0),
                ej_data.get('admins_size', 0),
                ej_data.get('directors_size', 0),
                ej_data.get('members_size', 0),
                ej_data.get('trainees_size', 0)
            ])
            time.sleep(0.3) # Pausa curta para não sobrecarregar o Portal
        except:
            continue

    # --- 6. ENVIO PARA O GOOGLE SHEETS ---
    print("\nSalvando tudo na planilha...")
    credentials_path = os.path.join(BASE_DIR, "credentials.json")
    
    try:
        sheets = SheetsService(credentials_path=credentials_path, spreadsheet_id=SPREADSHEET_ID)

        sheets.update_sheet("Dados Brutos", contracts_rows)
        
        if len(indicator_rows) > 1:
            sheets.update_sheet("Dados Brutos - Indicadores", indicator_rows)
            
        if len(member_rows) > 1:
            sheets.update_sheet("Dados Brutos - Membros", member_rows)

        print("🚀 Planilha atualizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar no Google: {e}")

if __name__ == "__main__":
    main()