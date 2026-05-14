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

# ============================================================
# SELECTORS - Login
# ============================================================
SEL_EMAIL = (By.ID, "input_3")
SEL_SENHA = (By.ID, "input_4")
SEL_BOTAO_LOGIN = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/div/div/div[2]/form/div[1]/input')

# ============================================================
# SELECTORS - Relatório Telegram (Communication Report)
# ============================================================
SEL_TIPO_ATENDIMENTO_TG = (By.XPATH, '//*[@id="select_value_label_31"]/span[1]')
SEL_TIPO_CHAT_TG = (By.XPATH, '//*[@id="select_option_35"]/div')
SEL_SELECTALL_STEP2_TG = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[2]/div[2]/report-metric-selector[2]/div[1]/md-checkbox/div[1]')
SEL_SELECTALL_STEP3_TG = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/report-metric-selector/div[1]/md-checkbox/div[1]')
SEL_INDIVIDUALCHAT_TG = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/div[2]/md-checkbox/div[1]')
SEL_DISPOSITIONS_TG = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/div[3]/md-checkbox/div[1]')
SEL_TIPO_PERIODO_TG = (By.XPATH, '//*[@id="select_value_label_32"]/span[1]')
SEL_PERIODO_PERSONALIZADO_TG = (By.XPATH, '//*[@id="select_option_147"]/div')
SEL_DATA_INI_TG = (By.XPATH, '//*[@id="from-date"]')
SEL_DATA_FIM_TG = (By.XPATH, '//*[@id="to-date"]')
SEL_DATA_GO_TG = (By.XPATH, '//*[@id="dialogContent_161"]/div[2]/button')
SEL_DOWNLOAD_TG = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/communication-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[5]/button')

# ============================================================
# SELECTORS - Relatório Timeline (Agent Report)
# ============================================================
SEL_ALL_AGENTS_TL = (By.XPATH, '//*[@id="radio_34"]/div[1]/div[1]')
SEL_TIPO_ATENDIMENTO_TL = (By.XPATH, '//*[@id="select_value_label_31"]/span[1]')
SEL_TIPO_CHAT_TL = (By.XPATH, '//*[@id="select_option_38"]/div')
SEL_SELECTALL_STEP3_TL = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/agent-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/report-metric-selector/div[1]/md-checkbox/div[1]')
SEL_AGENT_ACTIVITY_TL = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/agent-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[3]/div[2]/div[4]/md-checkbox/div[1]')
SEL_TIPO_PERIODO_TL = (By.XPATH, '//*[@id="select_value_label_32"]/span[1]')
SEL_PERIODO_PERSONALIZADO_TL = (By.XPATH, '//*[@id="select_option_155"]/div')
SEL_DATA_INI_TL = (By.XPATH, '//*[@id="from-date"]')
SEL_DATA_FIM_TL = (By.XPATH, '//*[@id="to-date"]')
SEL_DATA_GO_TL = (By.XPATH, '//*[@id="dialogContent_169"]/div[2]/button')
SEL_DOWNLOAD_TL = (By.XPATH, '//*[@id="single-spa-ujet-legacy"]/main/div/div/agent-report/div/div[2]/div/jt-setting/div/jt-setting-content/div/div[5]/button')


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
            raise TimeoutError("Tempo limite atingido aguardando o download terminar.")

        time.sleep(2)


def _clicar(wait, seletor, pausa=0.5):
    wait.until(EC.element_to_be_clickable(seletor)).click()
    sleep(pausa)


def extracao_bases_telegram(login, senha, url_home, url_telegram, url_timeline,
                            diretorio_download, data_inicio, data_final, logger=None):

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    navegador = webdriver.Edge(options=options)
    wait = WebDriverWait(navegador, 10)

    try:
        if logger:
            logger.info("Abrindo página de login")
        navegador.get(url_home)
        sleep(3)

        navegador.find_element(*SEL_EMAIL).send_keys(login)
        navegador.find_element(*SEL_SENHA).send_keys(senha)
        _clicar(wait, SEL_BOTAO_LOGIN, pausa=3)

        # ---------- Base Telegram ----------
        if logger:
            logger.info("Acessando página de relatórios Telegram")
        navegador.get(url_telegram)
        sleep(3)

        _clicar(wait, SEL_TIPO_ATENDIMENTO_TG)
        _clicar(wait, SEL_TIPO_CHAT_TG)
        _clicar(wait, SEL_SELECTALL_STEP2_TG)
        _clicar(wait, SEL_SELECTALL_STEP3_TG)
        _clicar(wait, SEL_INDIVIDUALCHAT_TG)
        _clicar(wait, SEL_DISPOSITIONS_TG)
        _clicar(wait, SEL_TIPO_PERIODO_TG)
        _clicar(wait, SEL_PERIODO_PERSONALIZADO_TG, pausa=1)

        wait.until(EC.element_to_be_clickable(SEL_DATA_INI_TG)).send_keys(
            data_inicio.strftime('%Y-%m-%d')
        )
        wait.until(EC.element_to_be_clickable(SEL_DATA_FIM_TG)).send_keys(
            data_final.strftime('%Y-%m-%d')
        )
        _clicar(wait, SEL_DATA_GO_TG)
        _clicar(wait, SEL_DOWNLOAD_TG)

        aguardar_download(diretorio_download, prefixos=("ChatReports-",), logger=logger)

        # ---------- Base Timeline ----------
        if logger:
            logger.info("Acessando página de relatórios Timeline")
        navegador.get(url_timeline)
        sleep(3)

        _clicar(wait, SEL_ALL_AGENTS_TL)
        _clicar(wait, SEL_TIPO_ATENDIMENTO_TL)
        _clicar(wait, SEL_TIPO_CHAT_TL)
        _clicar(wait, SEL_SELECTALL_STEP3_TL)
        _clicar(wait, SEL_AGENT_ACTIVITY_TL)
        _clicar(wait, SEL_TIPO_PERIODO_TL)
        _clicar(wait, SEL_PERIODO_PERSONALIZADO_TL)

        wait.until(EC.element_to_be_clickable(SEL_DATA_INI_TL)).send_keys(
            data_inicio.strftime('%Y-%m-%d')
        )
        wait.until(EC.element_to_be_clickable(SEL_DATA_FIM_TL)).send_keys(
            data_final.strftime('%Y-%m-%d')
        )
        sleep(0.5)
        _clicar(wait, SEL_DATA_GO_TL)
        _clicar(wait, SEL_DOWNLOAD_TL)

        aguardar_download(diretorio_download, prefixos=("AgentTeamReports-",), logger=logger)

        if logger:
            logger.info("Extração de bases concluída com sucesso")

    except Exception as e:
        if logger:
            logger.exception(f"Erro ao extrair bases: {e}")
        else:
            print(f"Erro ao extrair bases: {e}")

    finally:
        navegador.quit()
