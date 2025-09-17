from faker import Faker
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ---- Config ----
N_REGISTROS = 1000
CSV_PATH = "loja_informatica.csv"
SHOW_PLOTS = True
TOP_N = 5   # quantos produtos mostrar na pizza

# ---- Função de formatação em reais (pt-BR) ----
def fmt_brl(v):
    """Formata número float como R$ 1.234,56."""
    return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def make_df(n: int = N_REGISTROS) -> pd.DataFrame:
    faker = Faker("pt_BR")
    random.seed(42)
    produtos = ["Notebook", "Mouse", "Teclado", "Monitor",
                "Impressora", "HD Externo", "SSD", "Placa de Vídeo"]
    dados = []
    for _ in range(n):
        produto = random.choice(produtos)
        preco = round(random.uniform(100, 8000), 2)
        estoque = random.randint(1, 50)
        fornecedor = faker.company()
        dados.append({
            "Produto": produto,
            "Preço (R$)": preco,
            "Estoque": estoque,
            "Fornecedor": fornecedor
        })
    return pd.DataFrame(dados).convert_dtypes()

def save_csv_timed(df: pd.DataFrame, path: str) -> float:
    t0 = time.perf_counter()
    df.to_csv(path, index=False, encoding="utf-8")
    return time.perf_counter() - t0

if __name__ == "__main__":
    df = make_df()

    print("\nAmostra:")
    print(df.head())

    secs = save_csv_timed(df, CSV_PATH)
    print(f"\nCSV salvo em '{CSV_PATH}' em {secs:.4f}s")
    print(f"Linhas: {len(df)}  |  Colunas: {list(df.columns)}")

    if SHOW_PLOTS:
        df = pd.read_csv(CSV_PATH)

        print("\nTop 5 mais caros:")
        print(df.sort_values("Preço (R$)", ascending=False).head())

        print("\nEstoque total por produto:")
        print(df.groupby("Produto")["Estoque"].sum())

        print("\nPreço médio por produto:")
        # aplica formatação BRL ao mostrar
        preco_medio = df.groupby("Produto")["Preço (R$)"].mean()
        for produto, valor in preco_medio.items():
            print(f"{produto}: {fmt_brl(valor)}")

        # ---- Gráficos ----
        # 1) Estoque total (barra)
        estoque_total = df.groupby("Produto")["Estoque"].sum()
        estoque_total.plot(kind="bar", figsize=(8, 5))
        plt.title("Estoque Total por Produto")
        plt.ylabel("Quantidade")
        plt.xlabel("Produto")
        plt.show()

        # 2) Top N produtos mais caros (pizza)
        top_caros = preco_medio.sort_values(ascending=False).head(TOP_N)
        labels = [f"{nome} — {fmt_brl(v)}" for nome, v in top_caros.items()]
        plt.pie(top_caros, labels=labels, autopct="%1.1f%%")
        plt.title(f"Top {TOP_N} Produtos Mais Caros (Preço Médio)")
        plt.ylabel("")
        plt.show()

        # 3) Preço vs Estoque (dispersão)
        fig, ax = plt.subplots()
        ax.scatter(df["Preço (R$)"], df["Estoque"], alpha=0.6)
        ax.set_title("Preço vs Estoque")
        ax.set_xlabel("Preço (R$)")
        ax.set_ylabel("Estoque")
        # eixo X em reais
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: fmt_brl(x)))
        plt.tight_layout()
        plt.show()
