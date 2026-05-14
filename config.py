import os
from datetime import date

########### DIRETÓRIO RAIZ ###########
# Caminho absoluto para a pasta do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

########### DIRETÓRIOS ###########
# Pasta de origem e downloads dentro do projeto
DIRETORIO_ORIGEM = os.path.join(BASE_DIR, "downloads")
DIRETORIO_DOWNLOADS = DIRETORIO_ORIGEM

# Cria a pasta de downloads se não existir
os.makedirs(DIRETORIO_ORIGEM, exist_ok=True)

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

if hoje.day <= 5:
    if hoje.month == 1:
        data_inicio = date(hoje.year - 1, 12, 1)
    else:
        data_inicio = date(hoje.year, hoje.month - 1, 1)
else:
    data_inicio = date(hoje.year, hoje.month, 1)

data_final = hoje