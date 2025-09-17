import os, time
from teste01 import make_df

SAVE_TIME_MAX_SECONDS = float(os.getenv("SAVE_TIME_MAX_SECONDS", "2.0"))
N = int(os.getenv("DATA_ROWS_FOR_TEST", "1000"))

def test_tem_pelo_menos_500():
    df = make_df(N)
    assert len(df) >= 500

def test_save_csv_rapido(tmp_path):
    df = make_df(N)
    out = tmp_path / "out.csv"
    t0 = time.perf_counter()
    df.to_csv(out, index=False, encoding="utf-8")
    elapsed = time.perf_counter() - t0
    assert out.exists()
    assert elapsed <= SAVE_TIME_MAX_SECONDS, f"CSV levou {elapsed:.4f}s (> {SAVE_TIME_MAX_SECONDS}s)"