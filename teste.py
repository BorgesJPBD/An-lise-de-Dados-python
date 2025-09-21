import os, time
from teste01 import make_df

SAVE_TIME_MAX_SECONDS = float(os.getenv("SAVE_TIME_MAX_SECONDS", "2.0"))
N = int(os.getenv("DATA_ROWS_FOR_TEST", "1000"))


def test_tem_pelo_menos_500():
    df = make_df(N)
    assert len(df) >= 500


def test_salvamento_csv_rapido(tmp_path):
    df = make_df(N)
    arquivo_saida = tmp_path / "saida.csv" 
    tempo_inicial = time.perf_counter()
    df.to_csv(arquivo_saida, index=False, encoding="utf-8")
    tempo_gasto = time.perf_counter() - tempo_inicial
    assert arquivo_saida.exists()
    assert tempo_gasto <= SAVE_TIME_MAX_SECONDS, (
        f"CSV levou {tempo_gasto:.4f}s (> {SAVE_TIME_MAX_SECONDS}s)"
    )
