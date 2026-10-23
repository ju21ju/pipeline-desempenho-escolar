import pandas as pd
from pathlib import Path
df_alunos = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "raw"/"alunos.csv")
print("Alunos:", df_alunos.shape)
df_notas = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "raw"/"notas.csv")
print("Notas:", df_notas.shape)
df_freq = pd.read_csv(Path(__file__).resolve().parent.parent/ "data" / "raw"/"frequencia.csv")
print("Freq:", df_freq.shape)

print("alunos:", df_alunos.duplicated().sum())
print("notas:", df_notas.duplicated().sum())
print("freq:", df_freq.duplicated().sum())

print("alunos:", df_alunos.isna().sum())
print("notas:", df_notas.isna().sum())
print("freq:", df_freq.isna().sum())

print("turma:", df_alunos["turma"].value_counts())

df_notas.info()
print(df_notas["nota"].value_counts())
print("notas:", df_notas["nota"].str.contains(",").sum())