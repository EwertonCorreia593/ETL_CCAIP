import os
import logging
from config import DIRETORIO_ORIGEM

logger = logging.getLogger("CCAI")

def excluir_csvs_da_pasta(pasta: str = DIRETORIO_ORIGEM):

    arquivos = os.listdir(pasta)

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta, arquivo)

        if arquivo.lower().endswith(".csv"):
            try:
                os.remove(caminho_arquivo)
                logger.info(f"Arquivo CSV removido: {arquivo}")
            except Exception as e:
                logger.error(f"Erro ao remover {arquivo}: {e}")


def excluir_zips_antigos(pasta: str = DIRETORIO_ORIGEM):

    arquivos = os.listdir(pasta)

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta, arquivo)

        if (arquivo.startswith("ChatReports-") or arquivo.startswith("AgentTeamReports-")) and arquivo.lower().endswith(".zip"):
            try:
                os.remove(caminho_arquivo)
                logger.info(f"Arquivo ZIP removido: {arquivo}")
            except Exception as e:
                logger.error(f"Erro ao remover {arquivo}: {e}")