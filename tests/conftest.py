import os
import shutil
import tempfile
import pytest


@pytest.fixture
def pasta_temporaria():
    caminho = tempfile.mkdtemp()
    yield caminho
    shutil.rmtree(caminho, ignore_errors=True)


@pytest.fixture
def pasta_com_csvs(pasta_temporaria):
    for nome in ["arquivo1.csv", "dados.csv", "relatorio.csv"]:
        with open(os.path.join(pasta_temporaria, nome), "w") as f:
            f.write("col1,col2\n1,2")
    for nome in ["nota.txt", "imagem.png"]:
        with open(os.path.join(pasta_temporaria, nome), "w") as f:
            f.write("nao é csv")
    return pasta_temporaria
