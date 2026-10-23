# Pipeline de relatório de desempenho escolar

Pipeline em Python que limpa dados de alunos, notas e frequência de uma escola, calcula indicadores por turma e gera um relatório em Excel com um único comando.

> **Aviso:** os dados são **sintéticos**. Eles são criados por `src/gerar_dados.py`, com erros plantados de propósito (duplicatas, formatos inconsistentes, valores impossíveis) para exercitar a limpeza. Nenhum dado real de alunos foi usado.

## O problema

Escolas costumam receber notas e frequência em planilhas separadas, preenchidas à mão e cheias de inconsistências. Montar o relatório de cada bimestre exige limpar, juntar e calcular tudo de novo, o que é lento e difícil de repetir.

Este projeto automatiza esse fluxo: os dados brutos entram, e o relatório sai pronto, sempre com as mesmas regras.

## Como funciona

```
data/raw  ──►  limpeza  ──►  data/processed  ──►  métricas  ──►  reports/resumo_turmas.xlsx
 (brutos)   limpar_dados()     (limpos)      calcular_metricas()     (relatório)
```

1. **Limpeza** (`src/limpeza.py`): lê os arquivos brutos, corrige os problemas e grava os dados limpos em `data/processed`. Os arquivos originais nunca são alterados.
2. **Métricas e relatório** (`src/metricas.py`): lê só os dados limpos, junta as tabelas pelo `aluno_id`, calcula os indicadores por turma e exporta o resumo para Excel.
3. **Orquestração** (`main.py`): chama as duas etapas na ordem certa.

## Estrutura do projeto

```
desempenho_escolar/
├── data/
│   ├── raw/                # alunos.csv, notas.csv, frequencia.csv (gerados)
│   └── processed/          # alunos_limpos.csv, notas.csv, frequencia.csv (limpos)
├── reports/
│   └── resumo_turmas.xlsx  # relatório final
├── src/
│   ├── gerar_dados.py      # cria os dados sintéticos
│   ├── explorar.py         # exploração inicial dos dados brutos
│   ├── limpeza.py          # etapa de limpeza
│   └── metricas.py         # etapa de métricas e relatório
├── main.py                 # executa o pipeline completo
└── README.md
```

## Os dados

Três tabelas ligadas pelo `aluno_id`:

| Tabela | Conteúdo | Tamanho esperado |
|---|---|---|
| `alunos` | nome e turma | 240 alunos, 8 turmas (6A a 9B) |
| `notas` | nota por aluno, disciplina e bimestre | 5.760 linhas (240 × 6 disciplinas × 4 bimestres) |
| `frequencia` | aulas dadas e faltas, na mesma estrutura | 5.760 linhas |

## Decisões de limpeza

Cada tratamento foi uma escolha consciente:

| Problema encontrado | Quantidade | Decisão |
|---|---|---|
| Linhas duplicadas | 5 em alunos, 150 em notas, 150 em frequência | Removidas |
| Turmas escritas de dois jeitos (`8B` e `8º B`) | 16 valores para 8 turmas | Padronizadas no formato `8B` |
| Nomes com espaços sobrando e em maiúsculas | 30 nomes | Espaços removidos e capitalização padronizada |
| Notas com vírgula decimal (`3,2`) | 302 (antes de remover duplicatas) | Vírgula trocada por ponto; coluna convertida de texto para número |
| Notas fora do intervalo de 0 a 10 (como 100 e -1) | 15 | Marcadas como vazias, sem corrigir por chute e sem apagar a linha |
| Notas vazias | 185 ao final (170 originais + 15 invalidadas) | Mantidas vazias; as médias ignoram esses registros |
| Faltas maiores que as aulas dadas | 20 | Marcadas como vazias |
| Faltas vazias | — | Mantidas vazias, e não trocadas por 0, que diria que o aluno não faltou |

## Resultados (com os dados sintéticos)

| Turma | Média de notas | Média de faltas |
|---|---|---|
| 6A | 6,65 | 2,52 |
| 6B | 6,27 | 1,96 |
| 7A | 6,41 | 2,64 |
| 7B | 5,57 | 2,48 |
| 8A | 6,42 | 2,11 |
| 8B | 6,64 | 2,65 |
| 9A | 6,58 | 2,49 |
| 9B | 6,12 | 1,99 |

A média de faltas é por registro (disciplina e bimestre). Além do relatório em Excel, o pipeline mostra no terminal quantos alunos estão **em risco**, definidos como os que têm média geral abaixo de 5: **44 de 240** (cerca de 18%).

Observações: a 7B tem a menor média de notas, e a 8B é a turma que mais falta e, mesmo assim, tem uma das melhores médias.

## Como executar

Requisitos: Python 3 (desenvolvido com Python 3.14 e pandas 3.0) e as bibliotecas `pandas`, `numpy` e `openpyxl`.

```bash
# 1. Crie e ative um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 2. Instale as dependências
pip install pandas numpy openpyxl

# 3. Crie as pastas de saída (o Git não guarda pastas vazias)
mkdir data\processed reports   # Windows
# mkdir -p data/processed reports   # Linux/macOS

# 4. Gere os dados sintéticos (cria data/raw)
python src/gerar_dados.py

# 5. Rode o pipeline completo
python main.py
```

O relatório é gravado em `reports/resumo_turmas.xlsx`. Se o arquivo estiver aberto no Excel, feche-o antes de rodar de novo, pois o Windows bloqueia a gravação.

## Ferramentas

Python, pandas, numpy, openpyxl e PyCharm.

## Próximos passos

- [ ] Incluir a lista de alunos em risco numa segunda aba do Excel
- [ ] Registrar a execução em um arquivo de log, em vez de mensagens na tela
- [ ] Agendar a execução automática (por exemplo, com o Agendador de Tarefas do Windows)

## Autora

Juliana (Ju) Schmidt Moreira
