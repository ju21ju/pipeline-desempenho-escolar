import pandas as pd
from pathlib import Path
def calcular_metricas():


    df_alunos = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "processed"/"alunos_limpos.csv")

    df_alunos = df_alunos.drop_duplicates()


    df_notas = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "processed"/"notas.csv")

    df_notas = df_notas.drop_duplicates()


    df_freq = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "processed"/"frequencia.csv")

    df_freq = df_freq.drop_duplicates()


    df_notas_turma = df_notas.merge(df_alunos, on="aluno_id")


    media = df_notas_turma.groupby("turma")["nota"].mean()

    media_aluno = df_notas_turma.groupby("aluno_id")["nota"].mean()
    print("Alunos em risco:", (media_aluno < 5).sum())

    df_freq_turma = df_freq.merge(df_alunos, on="aluno_id")

    media_faltas_turma = df_freq_turma.groupby("turma")["faltas"].mean()

    resumo_turma = pd.DataFrame({
        "Média de notas": media,
        "Média de faltas": media_faltas_turma,
    })
    print("Resumo:", resumo_turma)

    resumo_turma = resumo_turma.round(2)
    resumo_turma.to_excel((Path(__file__).resolve().parent.parent/ "reports" / "resumo_turmas.xlsx"))
if __name__ == "__main__":
    calcular_metricas()
