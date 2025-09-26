from faker import Faker
import pandas as pd
import random, time, locale
import matplotlib.pyplot as plt



N_REGISTROS = 1000
ARQUIVO_CSV = "Estoque_loja_informatica.csv"
MOSTRAR_GRAFICOS = True
TOP_N = 5


locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8") 

def formatação_em_real(v):
    
    return locale.currency(v, grouping=True, symbol=True) 

def make_df(n: int = N_REGISTROS) -> pd.DataFrame:
    
    faker = Faker("pt_BR")
    random.seed(2)
    produtos = ["Notebook","Mouse","Teclado","Monitor","Impressora","HD Externo","SSD","Placa de Vídeo"]
    dados = [{
        "Produto": random.choice(produtos), 
        "Preço (R$)": round(random.uniform(100, 8000), 2), 
        "Estoque": random.randint(1, 50), 
        "Fornecedor": faker.company()
    } for _ in range(n)] 
    return pd.DataFrame(dados).convert_dtypes() 

def salvar_csv_temporizado(df: pd.DataFrame, ARQUIVO_CSV: str) -> float:  
    tempo = time.perf_counter() 
    df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8") 
    return time.perf_counter() - tempo 

if __name__ == "__main__":
    df = make_df() 
    print("\nAmostra:") 
    print(df.head())  

    secs = salvar_csv_temporizado(df, ARQUIVO_CSV)
    print(f"\nCSV salvo em '{ARQUIVO_CSV}' em {secs:.4f}s") 
    print(f"Linhas: {len(df)}")

    if MOSTRAR_GRAFICOS:
        df = pd.read_csv(ARQUIVO_CSV)

        print("\nTop 5 mais caros:")
        print(df.sort_values("Preço (R$)", ascending=False).head()) 

        print("\nEstoque total por produto:")
        print(df.groupby("Produto")["Estoque"].sum())  

        print("\nPreço médio por produto:")
        preco_medio = df.groupby("Produto")["Preço (R$)"].mean() 
        for produto, valor in preco_medio.items(): 
            print(f"{produto}: {formatação_em_real(valor)}") 

        
        df.groupby("Produto")["Estoque"].sum().plot(kind="bar", figsize=(8, 5))  
        plt.title("Estoque Total por Produto")
        plt.ylabel("Quantidade")
        plt.xlabel("Produto")
        plt.show()

        
        top_caros = preco_medio.sort_values(ascending=False).head(TOP_N) 
        labels = [f"{nome} — {formatação_em_real(v)}" for nome, v in top_caros.items()] #
        plt.pie(top_caros, labels=labels, autopct="%1.1f%%")
        plt.title(f"Top {TOP_N} Produtos Mais Caros (Preço Médio)")
        plt.show()



        

        

        
