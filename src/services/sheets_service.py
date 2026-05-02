import gspread
from google.oauth2.service_account import Credentials

class SheetsService:
    """
    O motor que conversa com o Google Sheets.
    """
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        # Permissões necessárias para ler e escrever
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]

        creds = Credentials.from_service_account_file(
            credentials_path,
            scopes=scopes
        )

        client = gspread.authorize(creds)
        self.sheet = client.open_by_key(spreadsheet_id)

    def update_sheet(self, worksheet_name: str, rows: list[list]):
        """
        Limpa a aba escolhida e escreve os novos dados.
        DICA: 'rows' já deve conter o cabeçalho na primeira posição!
        """
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
            
            # Limpa todo o conteúdo da aba
            worksheet.clear()

            # Escreve todas as linhas de uma vez só (mais rápido)
            if rows:
                worksheet.append_rows(rows)
                
        except Exception as e:
            print(f"Erro ao atualizar aba {worksheet_name}: {e}")