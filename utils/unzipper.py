import os
import logging
import zipfile

logger = logging.getLogger("CCAI")


def mes_do_zip(nome_arquivo):
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março",
        4: "Abril", 5: "Maio", 6: "Junho",
        7: "Julho", 8: "Agosto", 9: "Setembro",
        10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    try:
        partes = nome_arquivo.split("-")
        ano = int(partes[1])
        mes = int(partes[2])
        return meses[mes]
    except:
        return "MesDesconhecido"


def extrair_arquivos_especificos(pasta: str):
    arquivos = os.listdir(pasta)

    for arquivo in arquivos:
        caminho_zip = os.path.join(pasta, arquivo)

        if not arquivo.lower().endswith(".zip"):
            continue

        try:
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                nomes = zip_ref.namelist()
                mes = mes_do_zip(arquivo)

                messaging_files = [
                    n for n in nomes
                    if arquivo.startswith("ChatReports-")
                    and n.startswith("Messaging Inbound")
                    and n.endswith(".csv")
                ]

                activity_files = [
                    n for n in nomes
                    if arquivo.startswith("AgentTeamReports-")
                    and n.startswith("Activity Timeline -")
                    and n.endswith(".csv")
                ]

                # --- Messaging Inbound ---
                if len(messaging_files) == 1:
                    nome = messaging_files[0]
                    destino = os.path.join(pasta, f"messaging_inbound_{mes}.csv")
                    with zip_ref.open(nome) as origem, open(destino, "wb") as saida:
                        saida.write(origem.read())
                    logger.info(f"Extraído {nome} de {arquivo} para {destino}")
                elif len(messaging_files) > 1:
                    for i, nome in enumerate(messaging_files, start=1):
                        destino = os.path.join(pasta, f"messaging_inbound_{mes}_{i}.csv")
                        with zip_ref.open(nome) as origem, open(destino, "wb") as saida:
                            saida.write(origem.read())
                        logger.info(f"Extraído {nome} de {arquivo} para {destino}")

                # --- Activity Timeline ---
                if len(activity_files) == 1:
                    nome = activity_files[0]
                    destino = os.path.join(pasta, f"activity_timeline_{mes}.csv")
                    with zip_ref.open(nome) as origem, open(destino, "wb") as saida:
                        saida.write(origem.read())
                    logger.info(f"Extraído {nome} de {arquivo} para {destino}")
                elif len(activity_files) > 1:
                    for i, nome in enumerate(activity_files, start=1):
                        destino = os.path.join(pasta, f"activity_timeline_{mes}_{i}.csv")
                        with zip_ref.open(nome) as origem, open(destino, "wb") as saida:
                            saida.write(origem.read())
                        logger.info(f"Extraído {nome} de {arquivo} para {destino}")

        except Exception as e:
            logger.error(f"Erro ao extrair {arquivo}: {e}")
