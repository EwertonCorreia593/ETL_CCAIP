import os
import glob
import time
import shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import DOWNLOAD_TIMEOUT

# =============================================================================
# SELECTORS — Login
# =============================================================================
LOGIN_EMAIL = (By.ID, "input_3")
LOGIN_SENHA = (By.ID, "input_4")
LOGIN_BOTAO = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/div/div/div[2]/form/div[1]/input')

# =============================================================================
# SELECTORS — Relatório Telegram / Communication Report
# =============================================================================
TG_TIPO_ATENDIMENTO    = (By.XPATH, '//*[@id="select_value_label_32"]/span[1]')
TG_TIPO_CHAT           = (By.XPATH, '//*[@id="select_option_36"]/div')
TG_SELECTALL_STEP2     = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[2]/div[2]/report-metric-selector[2]/div[1]/md-checkbox/div[1]')
TG_SELECTALL_STEP3     = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/report-metric-selector/div[1]/md-checkbox/div[1]')
TG_INDIVIDUALCHAT      = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/div[2]/md-checkbox/div[1]')
TG_DISPOSITIONS        = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/div[3]/md-checkbox/div[1]')
TG_TIPO_PERIODO        = (By.XPATH, '//*[@id="select_value_label_33"]/span[1]')
TG_PERIODO_PERSONALIZ  = (By.XPATH, '//*[@id="select_option_148"]/div')
TG_DATA_INI            = (By.XPATH, '//*[@id="from-date"]')
TG_DATA_FIM            = (By.XPATH, '//*[@id="to-date"]')
TG_DATA_GO             = (By.XPATH, '//*[@id="dialogContent_162"]/div[2]/button')
TG_DOWNLOAD            = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[5]/button')

# =============================================================================
# SELECTORS — Relatório Timeline / Agent Report
# =============================================================================
TL_ALL_AGENTS          = (By.XPATH, '//*[@id="radio_35"]/div[1]/div[1]')
TL_TIPO_ATENDIMENTO    = (By.XPATH, '//*[@id="select_value_label_32"]/span[1]')
TL_TIPO_CHAT           = (By.XPATH, '//*[@id="select_option_39"]/div')
TL_SELECTALL_STEP3     = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/agent-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/report-metric-selector/div[1]/md-checkbox/div[1]')
TL_AGENT_ACTIVITY      = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/agent-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/div[4]/md-checkbox/div[1]')
TL_TIPO_PERIODO        = (By.XPATH, '//*[@id="select_value_label_33"]/span[1]')
TL_PERIODO_PERSONALIZ  = (By.XPATH, '//*[@id="select_option_156"]/div')
TL_DATA_INI            = (By.XPATH, '//*[@id="from-date"]')
TL_DATA_FIM            = (By.XPATH, '//*[@id="to-date"]')
TL_DATA_GO             = (By.XPATH, '//*[@id="dialogContent_170"]/div[2]/button')
TL_DOWNLOAD            = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/agent-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[5]/button/span')


# =============================================================================
# UTILITÁRIOS
# =============================================================================

def _clicar(wait, seletor, nome="", pausa=0.5):
    try:
        wait.until(EC.element_to_be_clickable(seletor)).click()
        sleep(pausa)
    except Exception as e:
        raise RuntimeError(f"Falha ao clicar em '{nome}'") from e


def aguardar_download(pasta_projeto, prefixos=("ChatReports-", "AgentReports-"), timeout=DOWNLOAD_TIMEOUT, logger=None):
    tempo_inicial = time.time()
    pasta_usuario = os.path.join(os.path.expanduser("~"), "Downloads")

    while True:
        arquivos_usuario = [
            f for f in os.listdir(pasta_usuario)
            if f.endswith(".zip") and f.startswith(prefixos)
        ]

        for arquivo in arquivos_usuario:
            origem = os.path.join(pasta_usuario, arquivo)
            destino = os.path.join(pasta_projeto, arquivo)
            try:
                shutil.move(origem, destino)
                if logger:
                    logger.info(f"Arquivo {arquivo} movido de Downloads para {pasta_projeto}")
            except Exception as e:
                if logger:
                    logger.warning(f"Erro ao mover {arquivo}: {e}")

        arquivos_zip = [f for f in os.listdir(pasta_projeto) if f.endswith(".zip")]
        encontrados = [f for f in arquivos_zip if f.startswith(prefixos)]
        downloads_em_andamento = glob.glob(os.path.join(pasta_projeto, "*.crdownload"))

        if encontrados and not downloads_em_andamento:
            if logger:
                logger.info(f"Download concluído: {encontrados}")
            return encontrados

        if time.time() - tempo_inicial > timeout:
            raise TimeoutError(f"Tempo limite de {timeout}s atingido aguardando download de {prefixos}")

        time.sleep(2)


# =============================================================================
# ETAPAS DA EXTRAÇÃO
# =============================================================================

def _login(navegador, wait, email, senha, url_home, logger=None, tentativas=3):
    if logger:
        logger.info("Login: acessando página de autenticação")
    navegador.get(url_home)

    for tentativa in range(1, tentativas + 1):
        if tentativa > 1 and logger:
            logger.info(f"Login: tentativa {tentativa}/{tentativas}")

        sleep(5)

        if logger:
            logger.info(f"Login: digitando email ({len(email)} caracteres)")

        wait.until(EC.element_to_be_clickable(LOGIN_EMAIL)).send_keys(email)
        sleep(0.5)
        wait.until(EC.element_to_be_clickable(LOGIN_SENHA)).send_keys(senha)
        sleep(0.5)

        _clicar(wait, LOGIN_BOTAO, nome="botão de login", pausa=3)

        try:
            WebDriverWait(navegador, 10).until(
                lambda d: url_home not in d.current_url
            )
            if logger:
                logger.info("Login: autenticação realizada com sucesso")
            return
        except:
            if logger:
                logger.warning("Login: falhou, tentando novamente...")

    raise RuntimeError("Login não autenticou após várias tentativas")


def _extrair_telegram(navegador, wait, url_telegram, diretorio_download, data_inicio, data_final, logger=None):
    if logger:
        logger.info("Telegram: acessando página de relatório de comunicação")
    navegador.get(url_telegram)
    sleep(3)

    _clicar(wait, TG_TIPO_ATENDIMENTO, nome="Telegram > tipo de atendimento")
    _clicar(wait, TG_TIPO_CHAT,        nome="Telegram > tipo chat")
    _clicar(wait, TG_SELECTALL_STEP2,  nome="Telegram > selecionar todos (step 2)")
    _clicar(wait, TG_SELECTALL_STEP3,  nome="Telegram > selecionar todos (step 3)")
    _clicar(wait, TG_INDIVIDUALCHAT,   nome="Telegram > chat individual")
    _clicar(wait, TG_DISPOSITIONS,     nome="Telegram > dispositions")
    _clicar(wait, TG_TIPO_PERIODO,     nome="Telegram > tipo de período")
    _clicar(wait, TG_PERIODO_PERSONALIZ, nome="Telegram > período personalizado", pausa=1)

    wait.until(EC.element_to_be_clickable(TG_DATA_INI)).send_keys(data_inicio.strftime('%Y-%m-%d'))
    wait.until(EC.element_to_be_clickable(TG_DATA_FIM)).send_keys(data_final.strftime('%Y-%m-%d'))
    _clicar(wait, TG_DATA_GO,   nome="Telegram > botão GO da data")
    _clicar(wait, TG_DOWNLOAD,  nome="Telegram > botão download")

    aguardar_download(diretorio_download, prefixos=("ChatReports-",), logger=logger)
    if logger:
        logger.info("Telegram: download do relatório concluído")


def _extrair_timeline(navegador, wait, url_timeline, diretorio_download, data_inicio, data_final, logger=None):
    if logger:
        logger.info("Timeline: acessando página de relatório de agente")
    navegador.get(url_timeline)
    sleep(3)

    _clicar(wait, TL_ALL_AGENTS,         nome="Timeline > todos os agentes")
    _clicar(wait, TL_TIPO_ATENDIMENTO,   nome="Timeline > tipo de atendimento")
    _clicar(wait, TL_TIPO_CHAT,          nome="Timeline > tipo chat")
    _clicar(wait, TL_SELECTALL_STEP3,    nome="Timeline > selecionar todos (step 3)")
    _clicar(wait, TL_AGENT_ACTIVITY,     nome="Timeline > atividade do agente")
    _clicar(wait, TL_TIPO_PERIODO,       nome="Timeline > tipo de período")
    _clicar(wait, TL_PERIODO_PERSONALIZ, nome="Timeline > período personalizado")

    wait.until(EC.element_to_be_clickable(TL_DATA_INI)).send_keys(data_inicio.strftime('%Y-%m-%d'))
    wait.until(EC.element_to_be_clickable(TL_DATA_FIM)).send_keys(data_final.strftime('%Y-%m-%d'))
    sleep(0.5)
    _clicar(wait, TL_DATA_GO,   nome="Timeline > botão GO da data")
    _clicar(wait, TL_DOWNLOAD,  nome="Timeline > botão download")

    aguardar_download(diretorio_download, prefixos=("AgentTeamReports-",), logger=logger)
    if logger:
        logger.info("Timeline: download do relatório concluído")


# =============================================================================
# ORQUESTRADOR PRINCIPAL
# =============================================================================

def extracao_bases_telegram(login, senha, url_home, url_telegram, url_timeline,
                            diretorio_download, data_inicio, data_final, logger=None):

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    navegador = webdriver.Edge(options=options)
    wait = WebDriverWait(navegador, 10)

    try:
        _login(navegador, wait, login, senha, url_home, logger)

        _extrair_telegram(navegador, wait, url_telegram, diretorio_download, data_inicio, data_final, logger)
        _extrair_timeline(navegador, wait, url_timeline, diretorio_download, data_inicio, data_final, logger)

        if logger:
            logger.info("Extração de bases concluída com sucesso")

    except RuntimeError as e:
        if logger:
            logger.error(f"extracao_bases_telegram: {e}")
        raise

    except TimeoutError as e:
        if logger:
            logger.error(f"extracao_bases_telegram: tempo limite — {e}")
        raise

    except Exception as e:
        if logger:
            logger.exception(f"extracao_bases_telegram: erro inesperado — {e}")
        raise

    finally:
        navegador.quit()
