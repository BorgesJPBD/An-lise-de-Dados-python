import time
from teste01 import make_df

TEMPO_GASTO = 2.0
LINHAS = 1000


def test_tem_pelo_menos_500():
    df = make_df(N)
    assert len(df) >= 500


def test_salvamento_csv_rapido(tmp_path):
    df = make_df(LINHAS)
    arquivo_saida = tmp_path / "saida.csv" 
    tempo_inicial = time.perf_counter()
    df.to_csv(arquivo_saida, index=False, encoding="utf-8")
    tempo_gasto = time.perf_counter() - tempo_inicial
    assert arquivo_saida.exists()
    assert tempo_gasto <= TEMPO_GASTO, (
        f"CSV levou {tempo_gasto:.4f}s (> {TEMPO_GASTO}s)"
    )
