import numpy as np
import pandas as pd
from pathlib import Path

# Gerador de números aleatórios (a "semente" 42 garante que os dados saiam iguais toda vez)
rng = np.random.default_rng(42)

# Caminho da pasta data/raw, calculado a partir da localização deste arquivo
PASTA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
PASTA_RAW.mkdir(parents=True, exist_ok=True)

TURMAS = ["6A", "6B", "7A", "7B", "8A", "8B", "9A", "9B"]
DISCIPLINAS = ["Matemática", "Português", "Ciências", "História", "Geografia", "Inglês"]
BIMESTRES = [1, 2, 3, 4]
N_ALUNOS = 240

primeiros = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda", "Felipe", "Gabriela", "Heitor",
             "Isabela", "João", "Larissa", "Mateus", "Natália", "Pedro", "Rafaela", "Thiago"]
sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Pereira", "Costa", "Ribeiro",
              "Almeida", "Ferreira", "Rodrigues", "Gomes", "Martins", "Araújo", "Barbosa"]

# ---------- Tabela de alunos ----------
nomes = [
    f"{rng.choice(primeiros)} {rng.choice(sobrenomes)} {rng.choice(sobrenomes)}"
    for _ in range(N_ALUNOS)
]
alunos = pd.DataFrame({
    "aluno_id": range(1, N_ALUNOS + 1),
    "nome": nomes,
    "turma": rng.choice(TURMAS, N_ALUNOS),
})

# ---------- Notas e frequência ----------
# Cada aluno tem um "nível" próprio, para os dados parecerem reais
nivel = pd.Series(rng.normal(6.5, 1.5, N_ALUNOS), index=alunos["aluno_id"])
taxa_faltas = pd.Series(rng.beta(1.5, 12, N_ALUNOS), index=alunos["aluno_id"])

base = pd.MultiIndex.from_product(
    [alunos["aluno_id"], DISCIPLINAS, BIMESTRES],
    names=["aluno_id", "disciplina", "bimestre"],
).to_frame(index=False)

notas = base.copy()
notas["nota"] = (notas["aluno_id"].map(nivel) + rng.normal(0, 1, len(notas))).clip(0, 10).round(1)

frequencia = base.copy()
frequencia["aulas_dadas"] = rng.integers(18, 26, len(frequencia))
frequencia["faltas"] = rng.binomial(frequencia["aulas_dadas"], frequencia["aluno_id"].map(taxa_faltas))

# ---------- Sujeira proposital (para treinarmos a limpeza) ----------
# alunos: nomes com espaços e MAIÚSCULAS, turmas em formatos diferentes, alunos repetidos
idx = rng.choice(N_ALUNOS, 30, replace=False)
alunos.loc[idx, "nome"] = "  " + alunos.loc[idx, "nome"].str.upper() + " "
idx = rng.choice(N_ALUNOS, 40, replace=False)
alunos.loc[idx, "turma"] = alunos.loc[idx, "turma"].str[0] + "º " + alunos.loc[idx, "turma"].str[1]
alunos = pd.concat([alunos, alunos.sample(5, random_state=1)], ignore_index=True)

# notas: vírgula no lugar do ponto, valores vazios, notas impossíveis e linhas duplicadas
notas["nota"] = notas["nota"].astype(object)
idx = rng.choice(len(notas), 300, replace=False)
notas.loc[idx, "nota"] = notas.loc[idx, "nota"].astype(str).str.replace(".", ",", regex=False)
notas.loc[rng.choice(len(notas), 170, replace=False), "nota"] = np.nan
notas.loc[rng.choice(len(notas), 15, replace=False), "nota"] = rng.choice([11, 15, 100, -1], 15)
notas = pd.concat([notas, notas.sample(150, random_state=2)], ignore_index=True)

# frequência: faltas vazias, faltas maiores que as aulas dadas, linhas duplicadas
frequencia["faltas"] = frequencia["faltas"].astype(float)
frequencia.loc[rng.choice(len(frequencia), 120, replace=False), "faltas"] = np.nan
idx = rng.choice(len(frequencia), 20, replace=False)
frequencia.loc[idx, "faltas"] = frequencia.loc[idx, "aulas_dadas"] + 5
frequencia = pd.concat([frequencia, frequencia.sample(150, random_state=3)], ignore_index=True)

# ---------- Salvar ----------
alunos.to_csv(PASTA_RAW / "alunos.csv", index=False)
notas.to_csv(PASTA_RAW / "notas.csv", index=False)
frequencia.to_csv(PASTA_RAW / "frequencia.csv", index=False)

print(f"alunos: {len(alunos)} linhas")
print(f"notas: {len(notas)} linhas")
print(f"frequencia: {len(frequencia)} linhas")