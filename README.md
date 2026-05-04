# Bot de Monitoramento - Núcleo Campinas (NuCa)

Este projeto é uma ferramenta de automação desenvolvida para facilitar a gestão de dados de **Instâncias do MEJ**. O bot se conecta à API da Brasil Júnior, coleta informações atualizadas e as organiza automaticamente em uma planilha do Google Sheets.

## O que o bot faz?

- **Auditoria de Contratos**: Busca todos os contratos (comuns e colaborativos) do ano corrente.
- **Indicadores Estratégicos**: Coleta dados de Faturamento, CSAT e ECM via Growth Report.
- **Censo de Membros**: Realiza um detalhamento individual por EJ, separando Administradores, Diretores, Membros e Trainees.

## Pré-requisitos

Antes de começar, você vai precisar de:

1.  **Python 3.10+** instalado.
2.  **Ambiente de Execução**: Você pode rodar este bot em sua máquina local ou em servidores de nuvem. No **Núcleo Campinas (NuCa)**, utilizamos o **PythonAnywhere** para manter as execuções organizadas e programadas.
3.  **Google Cloud Console**: Uma conta com as APIs do Google Sheets e Google Drive ativadas (veja o tutorial ao final deste manual).
4.  **Arquivo `credentials.json`**: O arquivo de chaves da sua conta de serviço do Google.
5.  **Acesso ao Portal Brasil Júnior**: CPF e senha com permissões para visualizar dados da sua instância.
6.  **Planilha Estruturada**: Sua planilha deve conter exatamente estas abas: `Dados Brutos`, `Dados Brutos - Indicadores` e `Dados Brutos - Membros`.

## Instalação e Configuração

1. **Clonar o repositório:**

   ```bash
   git clone [https://github.com/seu-usuario/modelo-monitoras-nuca.git](https://github.com/seu-usuario/modelo-monitoras-nuca.git)
   cd modelo-monitoras-nuca

   ```

2. **Criar e ativar o ambiente virtual (venv):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

   ```

3. **Instalar as dependências:**

   ```bash
   pip install -r requirements.txt

   ```

4. **Configurar o ambiente (`.env`):**
   - Copie o arquivo `.env.example` e renomeie a cópia para `.env`.
   - Abra o arquivo e preencha com seu CPF, senha do Portal BJ, o ID da sua planilha e o `INSTANCE_ID` do seu Núcleo.

5. **Credenciais do Google:**
   - Coloque o seu arquivo `credentials.json` (baixado do Google Cloud) na pasta raiz do projeto.
   - **Importante:** Abra esse arquivo JSON, copie o e-mail da conta de serviço (algo como `robo-monitoras@projeto.iam.gserviceaccount.com`) e **compartilhe sua planilha** com esse e-mail com permissão de **Editor**.

## Como executar

Se estiver rodando no **PythonAnywhere** ou em sua máquina local, certifique-se de que o ambiente virtual está ativo:

```bash
# Ativar o ambiente (caso não esteja)
source venv/bin/activate


# Rodar o bot
python3 main.py

```

## Estrutura do Projeto

- **`src/api/`**: Motores de comunicação com a API da Brasil Júnior.
- **`src/models/`**: Definição de como os dados (Contratos) são organizados.
- **`src/services/`**: Toda a inteligência de processamento e conexão com o Google Sheets.
- **`src/auth.py`**: Gerencia o login e a geração das chaves de acesso.
- **`src/config.py`**: Lê e valida as configurações que você colocou no arquivo `.env`.
- **`main.py`**: O coração do bot que coordena todos os fluxos de dados.

---

## Deu algo errado? (Troubleshooting)

- **Erro 403 (Acesso Negado)**: Verifique se você compartilhou a planilha com o e-mail do robô (passo 5 das credenciais) como **Editor**.
- **Erro de Login (401)**: Verifique se o CPF e a Senha no arquivo `.env` estão corretos.
- **Módulo não encontrado**: Você esqueceu de rodar o comando `pip install -r requirements.txt` ou de ativar o seu ambiente virtual (`venv`).
- **Erro 504 (Timeout)**: O portal da BJ pode estar instável ou sobrecarregado. Aguarde alguns minutos e tente rodar o bot novamente.

---

### Créditos e Histórico

Este projeto foi desenvolvido originalmente por **Matheus Seiji** (Diretor de Projetos da Conpec 2024 e Líder de G1 do NuCa 2025) e disponibilizado como modelo por **Larissa Soares** (Diretora de G&G da Conpec 2025 e Líder de G1 do NuCa 2026).

---

### Dica para o Git

Ao compartilhar este repositório, lembre-se de que o arquivo **`.env`** e o **`credentials.json`** nunca devem ser enviados para o GitHub (eles já estão bloqueados no `.gitignore`). Cada núcleo deve criar os seus próprios arquivos seguindo este manual.

---

### Passo a Passo: Configurando as Credenciais do Google

Para que o bot tenha permissão de escrever na sua planilha, siga estas etapas no **Google Cloud Console**:

1.  **Criar o Projeto**:
    - Acesse o [Google Cloud Console](https://console.cloud.google.com/).
    - Clique em **Selecionar um projeto** > **Novo Projeto**.
    - Dê um nome (ex: `Monitoras-NuCa`) e clique em **Criar**.

2.  **Ativar as APIs**:
    - No menu lateral, vá em **APIs e Serviços** > **Biblioteca**.
    - Pesquise e ative a **Google Sheets API**.
    - Pesquise e ative a **Google Drive API**.

3.  **Criar a Conta de Serviço (O "perfil" do bot)**:
    - Vá em **APIs e Serviços** > **Credenciais**.
    - Clique em **+ Criar Credenciais** > **Conta de Serviço**.
    - Preencha o nome, clique em **Criar e Continuar** e depois em **Concluir**.

4.  **Gerar o arquivo `credentials.json`**:
    - Na lista de "Contas de Serviço", clique no ícone do **lápis** ao lado da conta criada.
    - Vá na aba **Chaves** (Keys) > **Adicionar Chave** > **Criar nova chave**.
    - Escolha o formato **JSON** e clique em **Criar**.
    - Renomeie o arquivo baixado para `credentials.json` e coloque-o na pasta raiz do projeto.

5.  **Liberar acesso na Planilha**:
    - Abra o arquivo `credentials.json`, localize o campo `"client_email"` e copie o endereço de e-mail (terminado em `.gserviceaccount.com`).
    - Vá na sua planilha do Google, clique em **Compartilhar** e adicione esse e-mail como **Editor**.

```

```
