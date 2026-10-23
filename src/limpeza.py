import pandas as pd
from pathlib import Path
def limpar_dados():


    df_alunos = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "raw"/"alunos.csv")

    df_alunos = df_alunos.drop_duplicates()

    df_notas = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "raw"/"notas.csv")

    df_notas = df_notas.drop_duplicates()


    df_freq = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "raw"/"frequencia.csv")

    df_freq = df_freq.drop_duplicates()


    df_alunos["turma"] = df_alunos["turma"].str.replace("º ", "")



    df_alunos["nome"] = df_alunos["nome"].str.strip().str.title()


    df_notas["nota"] = df_notas["nota"].str.replace(",", ".")


    df_notas["nota"] = pd.to_numeric(df_notas["nota"])


    df_notas["nota"].min()

    df_notas["nota"].max()

    df_notas["nota"]= df_notas["nota"].where(df_notas["nota"].between(0, 10))



    df_freq["faltas"] = df_freq["faltas"].where(df_freq["faltas"] <= df_freq["aulas_dadas"])


    caminho_alunos = Path(__file__).resolve().parent.parent/ "data" / "processed"/"alunos_limpos.csv"
    df_alunos.to_csv(caminho_alunos, index=False)
    caminho_freq = Path(__file__).resolve().parent.parent/ "data" / "processed"/"frequencia.csv"
    df_freq.to_csv(caminho_freq, index=False)
    caminho_notas = Path(__file__).resolve().parent.parent/ "data" / "processed"/"notas.csv"
    df_notas.to_csv(caminho_notas, index=False)

if __name__ == "__main__":
    limpar_dados()