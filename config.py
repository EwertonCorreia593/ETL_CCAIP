import os
from datetime import date, timedelta

########### DIRETÓRIO RAIZ ###########
# Caminho absoluto para a pasta do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

########### DIRETÓRIOS ###########
# Pasta de origem e downloads dentro do projeto
DIRETORIO_ORIGEM = os.path.join(BASE_DIR, "downloads")
DIRETORIO_DOWNLOADS = DIRETORIO_ORIGEM

# Cria a pasta de downloads se não existir
os.makedirs(DIRETORIO_ORIGEM, exist_ok=True)

########### DIRETÓRIOS DE SAÍDA (CSVs processados) ###########
# Diretório específico para messaging_inbound (opcional)
# Se não informado, o CSV fica na mesma pasta do ZIP
DIRETORIO_MESSAGING = os.getenv("CCAI_DIRETORIO_MESSAGING")
if DIRETORIO_MESSAGING:
    os.makedirs(DIRETORIO_MESSAGING, exist_ok=True)

# Diretório específico para activity_timeline (opcional)
# Se não informado, o CSV fica na mesma pasta do ZIP
DIRETORIO_ACTIVITY = os.getenv("CCAI_DIRETORIO_ACTIVITY")
if DIRETORIO_ACTIVITY:
    os.makedirs(DIRETORIO_ACTIVITY, exist_ok=True)

########### URLS ###########
URL_HOME = "https://bot-gare-vtal-iu1ezbt.sae1.ccaiplatform.com/sign-in"
URL_RELATORIOS_TELEGRAM = "https://bot-gare-vtal-iu1ezbt.sae1.ccaiplatform.com/reports/communication"
URL_RELATORIOS_TIMELINE = "https://bot-gare-vtal-iu1ezbt.sae1.ccaiplatform.com/reports/agent"

########### LOGIN ###########
LOGIN_EMAIL = os.getenv("CCAI_EMAIL", "")
SENHA = os.getenv("CCAI_SENHA", "")

########### TIMEOUT DOWNLOAD ###########
DOWNLOAD_TIMEOUT = int(os.getenv("CCAI_DOWNLOAD_TIMEOUT", "900"))

########### WEBDRIVER ###########
# Selenium Manager gerencia o driver automaticamente (Selenium 4.6+)
# Não é necessário baixar msedgedriver.exe manualmente

########### BANCO DE DADOS ###########
# Configuração movida para módulo específico (não utilizado nesta pipeline)

########### DATAS ###########
hoje = date.today()

# Reprocessamento manual: se as env vars estiverem setadas, usa as datas customizadas
data_inicio_env = os.getenv("CCAI_DATA_INICIO")
data_final_env = os.getenv("CCAI_DATA_FINAL")

if data_inicio_env and data_final_env:
    data_inicio = date.fromisoformat(data_inicio_env)
    data_final = date.fromisoformat(data_final_env)
else:
    # Padrão: últimos 5 dias
    data_inicio = hoje - timedelta(days=5)
    data_final = hoje