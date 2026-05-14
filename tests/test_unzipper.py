import os
import zipfile
from utils.unzipper import mes_do_zip, extrair_arquivos_especificos


class TestMesDoZip:
    def test_mes_5_retorna_maio(self):
        assert mes_do_zip("ChatReports-2026-5-1.zip") == "Maio"

    def test_mes_1_retorna_janeiro(self):
        assert mes_do_zip("ChatReports-2026-1-15.zip") == "Janeiro"

    def test_mes_12_retorna_dezembro(self):
        assert mes_do_zip("ChatReports-2025-12-31.zip") == "Dezembro"

    def test_nome_invalido_retorna_desconhecido(self):
        assert mes_do_zip("arquivo_invalido.zip") == "MesDesconhecido"

    def test_sem_extensao_retorna_desconhecido(self):
        assert mes_do_zip("apenas_um_nome") == "MesDesconhecido"


class TestExtrairArquivosEspecificos:
    def _criar_zip(self, pasta, nome_zip, arquivos_internos):
        caminho = os.path.join(pasta, nome_zip)
        with zipfile.ZipFile(caminho, "w") as zf:
            for nome_interno, conteudo in arquivos_internos:
                zf.writestr(nome_interno, conteudo)
        return caminho

    def test_extrai_messaging_inbound_de_chat_report(self, pasta_temporaria):
        self._criar_zip(pasta_temporaria, "ChatReports-2026-5-1.zip", [
            ("Messaging Inbound.csv", "col1,col2\na,b"),
            ("outro_arquivo.csv", "x,y"),
        ])

        extrair_arquivos_especificos(pasta_temporaria)

        arquivos = os.listdir(pasta_temporaria)
        assert "messaging_inbound_Maio.csv" in arquivos
        conteudo = open(os.path.join(pasta_temporaria, "messaging_inbound_Maio.csv")).read()
        assert conteudo == "col1,col2\na,b"

    def test_extrai_activity_timeline_de_agent_report(self, pasta_temporaria):
        self._criar_zip(pasta_temporaria, "AgentTeamReports-2026-5-1.zip", [
            ("Activity Timeline - All.csv", "col1,col2\nc,d"),
        ])

        extrair_arquivos_especificos(pasta_temporaria)

        arquivos = os.listdir(pasta_temporaria)
        assert "activity_timeline_Maio.csv" in arquivos

    def test_ignora_zip_que_nao_corresponde(self, pasta_temporaria):
        self._criar_zip(pasta_temporaria, "OutroRelatorio-2026-5.zip", [
            ("Messaging Inbound.csv", "dados"),
        ])

        extrair_arquivos_especificos(pasta_temporaria)

        assert os.listdir(pasta_temporaria) == ["OutroRelatorio-2026-5.zip"]

    def test_pasta_sem_zip_nao_quebra(self, pasta_temporaria):
        extrair_arquivos_especificos(pasta_temporaria)
        assert os.listdir(pasta_temporaria) == []
