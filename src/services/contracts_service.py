from src.models.contract import Contract
from datetime import datetime

class ContractsService:
    """
    O Serviço de Contratos sabe navegar por todas as páginas de contratos
    do núcleo e transformar as informações brutas em objetos organizados.
    """
    def __init__(self, client):
        self.client = client

    def get_contracts(self, instance_id: int, year: int, only_approved: bool = True):
        # Endereço específico para buscar contratos do núcleo (Core)
        endpoint = f"/portal/instances/cores/{instance_id}/contracts"

        page = 1
        per_page = 600 # Busca 600 contratos de uma vez para ir mais rápido
        last_page = False
        contracts = []

        # O bot vai lendo página por página até chegar na última
        while not last_page:
            params = {
                "page": page,
                "per_page": per_page,
                "q[from_year]": year,
                "q[s]": "signature_date asc"
            }

            response = self.client.get(endpoint, params=params)
            last_page = response["pagination"]["last_page"]

            for item in response["records"]:
                # Filtra apenas os aceitos/aprovados se a configuração estiver ativa
                if not only_approved or item["status"] == "accepted":
                    contracts.append(self._adapt_contract(item))

            page += 1

        return contracts

    def _adapt_contract(self, raw: dict) -> Contract:
        """
        Traduz o 'economês' da API da BJ para o formato do nosso robô.
        """
        # Transforma a data de texto (ISO) para formato de data real
        date_obj = datetime.fromisoformat(raw["signature_date"])

        colab_revenue = 0
        environment_agent = ""

        # Lógica para tratar contratos colaborativos (onde várias EJs participam)
        if raw["is_collaborative"]:
            kinds = []
            for colab in raw["contract_collaborations"]:
                colab_revenue += colab["revenue"]
                kinds.append(colab["kind"])
    
            # Junta os nomes dos agentes sem repetir (ex: 'Agente de Mercado, Outro Núcleo')
            environment_agent = ", ".join(set(kinds))

        return Contract(
            id=raw["id"],
            ej=raw["ej"]["name"],
            day=date_obj.day,
            month=date_obj.month,
            year=date_obj.year,
            solutions=len(raw["solutions"]),
            # O faturamento líquido da EJ é o total menos a parte colaborativa
            revenue=raw["revenue"] - colab_revenue,
            colab=raw["is_collaborative"],
            colab_revenue=colab_revenue,
            environment_agent=environment_agent
        )