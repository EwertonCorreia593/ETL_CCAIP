import os
import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv

load_dotenv(encoding="utf-8-sig")
from utils.unzipper import extrair_arquivos_especificos
from utils.selenium_extractor import extracao_bases_telegram
from utils.file_manager import (excluir_csvs_da_pasta,excluir_zips_antigos)
from config import (
    DIRETORIO_DOWNLOADS,
    DIRETORIO_MESSAGING, DIRETORIO_ACTIVITY,
    LOGIN_EMAIL, SENHA,
    URL_HOME, URL_RELATORIOS_TELEGRAM, URL_RELATORIOS_TIMELINE,
    data_inicio, data_final
)

# -------------------- Logger --------------------
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("CCAI")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = TimedRotatingFileHandler(
    "logs/ccai.log", when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def main():
    logger.info("Iniciando processo CCAI")

    try:
        # 1. Limpar CSVs e zips antigos
        excluir_csvs_da_pasta(DIRETORIO_DOWNLOADS)
        excluir_zips_antigos(DIRETORIO_DOWNLOADS)
        logger.info("Limpeza de arquivos antigos concluída")

        # 2. Extrair bases via Selenium
        extracao_bases_telegram(
            login=LOGIN_EMAIL,
            senha=SENHA,
            url_home=URL_HOME,
            url_telegram=URL_RELATORIOS_TELEGRAM,
            url_timeline=URL_RELATORIOS_TIMELINE,
            diretorio_download=DIRETORIO_DOWNLOADS,
            data_inicio=data_inicio,
            data_final=data_final,
            logger=logger
        )
        logger.info("Download das bases concluído")

        # 3. Extrair CSVs específicos dos zips
        total = extrair_arquivos_especificos(
            DIRETORIO_DOWNLOADS,
            destino_messaging=DIRETORIO_MESSAGING,
            destino_activity=DIRETORIO_ACTIVITY,
        )

        if total == 0:
            logger.error("Nenhum arquivo foi extraído — processo finalizado com erros")
            return

        logger.info("Processo finalizado com sucesso")

    except Exception as e:
        logger.exception("Erro durante execução do processo")

if __name__ == "__main__":
    main()
