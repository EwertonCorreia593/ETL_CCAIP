import os
from utils.file_manager import excluir_csvs_da_pasta, excluir_zips_antigos


def test_excluir_csvs_remove_apenas_csv(pasta_com_csvs):
    excluir_csvs_da_pasta(pasta_com_csvs)

    restantes = os.listdir(pasta_com_csvs)
    assert all(not f.lower().endswith(".csv") for f in restantes)
    assert "nota.txt" in restantes
    assert "imagem.png" in restantes


def test_excluir_csvs_pasta_vazia(pasta_temporaria):
    excluir_csvs_da_pasta(pasta_temporaria)
    assert os.listdir(pasta_temporaria) == []


def test_excluir_zips_antigos_remove_corretos(pasta_temporaria):
    zips_para_remover = ["ChatReports-2026-5.zip", "AgentTeamReports-2026-5.zip"]
    zips_manter = ["OutroRelatorio.zip", "dados.zip"]

    for nome in zips_para_remover + zips_manter:
        with open(os.path.join(pasta_temporaria, nome), "w") as f:
            f.write("fake zip")

    excluir_zips_antigos(pasta_temporaria)

    restantes = os.listdir(pasta_temporaria)
    for nome in zips_manter:
        assert nome in restantes
    for nome in zips_para_remover:
        assert nome not in restantes


def test_excluir_zips_antigos_sem_zip(pasta_temporaria):
    with open(os.path.join(pasta_temporaria, "arquivo.txt"), "w") as f:
        f.write("apenas texto")
    excluir_zips_antigos(pasta_temporaria)
    assert os.listdir(pasta_temporaria) == ["arquivo.txt"]
