# Acessibilidade Geográfica às UBS de Teresina

Roteiro computacional aberto e reprodutível que aplica o método **AE2SFCA**
(*Areal Enhanced Two-Step Floating Catchment Area*) para mensurar a acessibilidade
geográfica às Unidades Básicas de Saúde (UBS) da zona urbana de Teresina-PI, nos
modos automóvel e pedestre, e diagnosticar as desigualdades socioespaciais de acesso.

> Dissertação de Mestrado — [MAPEPROF](https://www.ifpi.edu.br/mapeprof)/IFPI — Felipe Ramos Dantas (2026)

| | |
|---|---|
| **Código** | <https://github.com/felipedantas-pi/ae2sfca-ubs> |
| **DOI do código** | [PREENCHER: DOI gerado pelo Zenodo a partir do *release* do GitHub] |
| **Dados** | [10.5281/zenodo.22964753](10.5281/zenodo.22964753) — descrição completa em [`docs/README_DATASET.md`](docs/README_DATASET.md) |
| **Dissertação** | [PREENCHER: link do repositório institucional do IFPI] |
| **Licenças** | Código: MIT · Texto, figuras e tabelas: CC BY 4.0 · Dados de terceiros: licença de cada origem |

## Sumário

1. [Início rápido](#início-rápido)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação](#instalação)
4. [Dados](#dados)
5. [Pipeline](#pipeline)
6. [Fontes e versões fixadas](#fontes-e-versões-fixadas)
7. [Verificando a replicação](#verificando-a-replicação)
8. [Estrutura do repositório](#estrutura-do-repositório)
9. [Método e hipóteses](#método-e-hipóteses)
10. [Reprodutibilidade e limitações](#reprodutibilidade-e-limitações)
11. [Solução de problemas](#solução-de-problemas)
12. [Como citar](#como-citar) · [Licença](#licença) · [Sobre o programa](#sobre-o-programa) · [Contato](#contato)

## Início rápido

```bash
git clone https://github.com/felipedantas-pi/ae2sfca-ubs.git
cd ae2sfca-ubs
uv sync                          # cria o ambiente (.venv) com as dependências fixadas
# baixe o dataset do Zenodo e extraia na raiz do repositório (seção "Dados")
uv run jupyter lab               # abra notebooks/ e execute em ordem
```

## Pré-requisitos

| Item | Requisito |
|---|---|
| Python | **3.12 ou superior** (o `uv` instala sozinho; ver `.python-version`) |
| Gerenciador | [`uv`](https://docs.astral.sh/uv/) |
| Sistema operacional | Desenvolvido e testado em **Windows 11**. Linux/macOS: [PREENCHER: "não testado" ou versões testadas] |
| GPU | **Não é necessária** (o treinamento da GNN roda em CPU) |
| Memória RAM | [PREENCHER: RAM mínima medida] |
| Espaço em disco | Ambiente Python (inclui PyTorch): [PREENCHER: GB] · Dataset do Zenodo: ~100 MB · Rota C (aquisição do zero): [PREENCHER: GB] adicionais para downloads |
| Internet | Só na **Rota C** (ver "Dados"). As Rotas A e B funcionam offline após baixar o dataset |

## Instalação

### Instalando o `uv`

O `uv` gerencia ambiente e dependências. **Não é preciso instalar o Python à parte**, o próprio
`uv` cuida disso.

**Windows (PowerShell)**

1. Abra o **PowerShell**: tecle `Win`, digite *PowerShell* e clique para abrir.
2. Cole o comando oficial de instalação e tecle `Enter`:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   > Alternativa (com o gerenciador *winget*): `winget install --id=astral-sh.uv`

3. **Feche e reabra** o PowerShell, para o sistema reconhecer o novo comando.
4. Confirme: `uv --version` (deve aparecer algo como `uv 0.x.x`).

**Linux / macOS**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Instalando o projeto

```bash
git clone https://github.com/felipedantas-pi/ae2sfca-ubs.git
cd ae2sfca-ubs
uv sync
```

O `uv sync` lê `pyproject.toml` e `uv.lock` e instala as versões exatas das bibliotecas
(incluindo `city2graph==0.3.1`) e o pacote local `mapeprof` (`src/mapeprof/`). A primeira
execução baixa o PyTorch e pode levar vários minutos.

Para abrir os notebooks: `uv run jupyter lab` (ou abra a pasta no Positron/VS Code e selecione
o interpretador `.venv`).

## Dados

Os dados **não são versionados no GitHub**. Eles ficam no **Zenodo** ([10.5281/zenodo.22964753](10.5281/zenodo.22964753)),
em um único pacote com a pasta `dados/` pronta (~100 MB descompactado). A pasta segue esta
estrutura, que os notebooks esperam (caminhos definidos em `src/mapeprof/config.py`):

```
dados/
├── externos/          # entradas de terceiros — NÃO MODIFICAR
│   ├── pmt/           #   camadas da Prefeitura (SEMPLAN): UBS e áreas de atuação (manuais)
│   ├── cnes/          #   Base CNES (competência 202604), reduzida à tabela de equipes
│   ├── ibge/          #   município, zona urbana e área de estudo (zona urbana + buffer de 5 km)
│   └── overture/      #   segmentos e conectores viários (Overture Maps)
├── intermediarios/    # saídas de cada notebook (regeneráveis)
│   ├── 01_malha/  02_grafo/  03_ubs/  04_impedancias/  05_isocronas/
└── processados/       # produto final: índice de acessibilidade por setor
```

### Escolha uma rota

| Rota | Objetivo | Notebooks | Internet | Tempo aproximado |
|---|---|---|---|---|
| **A: rápida** | Conferir o índice e os testes das hipóteses | apenas `05.1` e `06.1` | não | [PREENCHER: min] |
| **B: completa, offline** | Reproduzir todo o processamento a partir das entradas | `01.3` → `06.1` (`01.4` e `01.5` opcionais) | não | [PREENCHER: total medido] |
| **C: do zero** | Repetir também a aquisição dos dados públicos | `01.1` → `06.1` | **sim** | [PREENCHER: total medido] |

### Rotas A e B: baixar e extrair o dataset

Baixe `ae2sfca-ubs_dados_v1.0.zip` do Zenodo e extraia **na raiz do repositório** (o ZIP já
contém a pasta `dados/`).

**Windows (PowerShell)**

```powershell
Invoke-WebRequest -Uri "https://zenodo.org/records/10.5281/zenodo.22964753/files/ae2sfca-ubs_dados_v1.0.zip?download=1" -OutFile ae2sfca-ubs_dados_v1.0.zip
Expand-Archive -Path .\ae2sfca-ubs_dados_v1.0.zip -DestinationPath .
```

A integridade pode ser conferida com o `MANIFEST.csv` do registro (SHA-256 de cada arquivo):
`Get-FileHash -Algorithm SHA256 <arquivo>` (PowerShell) ou `sha256sum <arquivo>` (Linux/macOS).

Em seguida, execute os notebooks na ordem indicada na tabela acima. Na Rota B, o `01.3` reconhece
o ZIP do CNES já presente em `dados/externos/cnes/` e **não baixa** os ~700 MB do DataSUS.

### Rota C: do zero

Nesta rota os notebooks `01.1` (IBGE), `01.2` (Overture) e `01.3` (CNES) baixam os dados públicos.
Duas etapas são manuais:

1. **Crie o esqueleto de pastas** (os notebooks gravam em `dados/externos/…`, mas não criam essas pastas):

   ```powershell
   New-Item -ItemType Directory -Force -Path dados/externos/ibge, dados/externos/overture, dados/externos/cnes, dados/externos/pmt | Out-Null
   ```

   ```bash
   mkdir -p dados/externos/{ibge,overture,cnes,pmt}
   ```

2. **Obtenha as camadas da Prefeitura** (próxima seção) ou copie-as do pacote do Zenodo para `dados/externos/pmt/`.

> O `01.1` também baixa camadas auxiliares (bairros, grade estatística e CNEFE) descritas no
> Apêndice A da dissertação. Elas **não alimentam** os notebooks seguintes.

### Aquisição manual das camadas da Prefeitura (SEMPLAN)

As únicas camadas sem download automático vêm do geoportal **TeresinaGeo** (Prefeitura de
Teresina / SEMPLAN), que disponibiliza os dados apenas para visualização. Procedimento:

1. No geoportal, exporte as camadas em **KML** (formato nativo da plataforma).
   - Geoportal: https://www.google.com/maps/d/u/0/viewer?mid=1hz-s5m9BZJNf3hqztH5SKVT6DlNaoAte&ll=-5.08978475802348%2C-42.765517773528074&z=13
   - Data da exportação usada na dissertação: [06/04/2026]
2. Converta cada **KML → GeoJSON** (no QGIS: *Exportar → Salvar feições como… GeoJSON*; ou
   `ogr2ogr`), mantendo o CRS geográfico **EPSG:4326** (os notebooks reprojetam para UTM).
3. Salve em `dados/externos/pmt/` com **exatamente** estes nomes:

| Camada | Arquivo exigido | Geometria | Conteúdo mínimo esperado |
|---|---|---|---|
| Unidades Básicas de Saúde (93) | `ubs.geojson` | ponto | código CNES (`cnes`), nome, endereço |
| Áreas de atuação das ESF (240) | `area_das_esf.geojson` | polígono | `cnes`, `esf`, `nm_equipe`, `ine` |
| Áreas de atuação das UBS (75) | `area_das_ubs.geojson` | polígono | `cnes` e **`regional`** (SUL, NORTE, LESTE, SUDESTE) |

> ⚠️ **Os nomes de arquivo são obrigatórios.** Com outro nome, o `01.3` não encontra a camada e
> o pipeline para. A **capacidade** (nº de equipes) não vem dessas camadas: é calculada no `01.3`
> a partir da Base CNES, cruzando pelo código CNES de cada UBS.
>
> [PREENCHER: nota sobre autorização de uso/redistribuição das camadas da SEMPLAN, se houver]

## Pipeline

Execute os notebooks **em ordem**. Cada notebook lê as saídas do anterior. Os apêndices A–I
correspondem aos notebooks da dissertação; `01.4` e `01.5` são complementares (não integram os
apêndices) e não alteram a cadeia de cálculo.

| Notebook | Etapa | Lê (principais) | Grava (principais) | Tempo | Apêndice |
|---|---|---|---|---|---|
| `01.1` | Limites IBGE, setores censitários e demanda (Censo 2022) | download IBGE | `externos/ibge/*`, `01_malha/…DadosCompletos` | ~10–15 min | A |
| `01.2` | Malha viária (Overture Maps) | área de estudo (`ibge/`) e API Overture | `externos/overture/*` | [PREENCHER] | B |
| `01.3` | UBS e capacidade instalada (CNES) | `pmt/*`, ZIP do CNES (baixa se ausente) | `03_ubs/…ubs_capacidade` | [PREENCHER] | C |
| `01.4` | Visualização cartográfica da área de estudo | `ibge/`, `overture/`, UBS | figuras e tabela `nb014` | [PREENCHER] | — |
| `01.5` | Análise exploratória socioeconômica | `DadosCompletos`, UBS | figuras e tabelas `nb015` | [PREENCHER] | — |
| `02.1` | Limpeza e correção topológica da malha | `overture/*.geojson` | `02_grafo/…road_cleaned` | [PREENCHER] | D |
| `02.2` | Imputação de classes funcionais (Rede Neural em Grafos) | `road_cleaned` | `02_grafo/…road_imputed` | [PREENCHER] | E |
| `03.1` | Velocidades e impedâncias (tempo de viagem) | `road_imputed` | `04_impedancias/…road_routed` | [PREENCHER] | F |
| `04.1` | Isócronas de 10/20/30 min (carro e pedestre) | `road_routed`, UBS | `05_isocronas/*` | ~20–25 min | G |
| `05.1` | Índice AE2SFCA (e E2SFCA por centroide) | isócronas, UBS, `DadosCompletos` | `processados/…setores_acessibilidade` | [PREENCHER] | H |
| `06.1` | Testes das hipóteses (H1 socioterritorial e H2 metodológica) | `setores_acessibilidade`, `DadosCompletos` | figuras e tabelas `nb061` | [PREENCHER] | I |


Figuras e tabelas de cada notebook são gravadas em `outputs/figuras/nbXYZ/` e
`outputs/tabelas/nbXYZ/` (por exemplo, `nb051` = notebook 05.1).

## Fontes e versões fixadas

| Origem | Versão fixada | Onde é fixada |
|---|---|---|
| IBGE — Censo Demográfico 2022 (malhas CD2022; agregados por setor: população `V01006`; renda do responsável `V06004`/`V06006`) | arquivo de renda `..._20260508_csv.zip` | `01.1` |
| Overture Maps Foundation (temas `segment` e `connector`) | release **`2026-06-17.0`** | `01.2` (`RELEASE_OVERTURE`) |
| CNES/DataSUS — Base de Dados (tabela `tbEquipe`) | competência **`202604`** | `01.3` (`COMPETENCIA_CNES`) |
| Prefeitura de Teresina / SEMPLAN — UBS e áreas de atuação | exportação de [PREENCHER: data] | manual |
| `city2graph` | `0.3.1` | `pyproject.toml` |

Sistema de referência: **SIRGAS 2000 / UTM 23 Sul (EPSG:31983)** nos cálculos e nos arquivos derivados.

## Verificando a replicação

Após executar os notebooks, os valores abaixo devem coincidir com a dissertação
(`outputs/tabelas/nb051/` e `outputs/tabelas/nb061/`):

| Grandeza | Valor esperado | Arquivo |
|---|---|---|
| Setores urbanos / com dado válido de renda | 1.375 / 1.340 | `01.1` |
| UBS na área de estudo / equipes de APS | 81 / 474 | `01.3` |
| Índice médio, automóvel (equipes por 10 mil hab.) | 5,85 (mediana 6,09) | `nb051_sintese_indice.csv` |
| Índice médio, pedestre (equipes por 10 mil hab.) | 5,62 (mediana 5,79) | `nb051_sintese_indice.csv` |
| Setores classificados como "deserto de saúde": automóvel / pedestre | 344 / 358 | `nb051_sintese_indice.csv` |
| **H1:** Spearman acesso × renda mediana: automóvel / pedestre | +0,438 / −0,199 | `nb061_h1_sintese.csv` |
| **H2:** Spearman AE2SFCA × E2SFCA: automóvel / pedestre | 0,991 / 0,949 | `nb061_h2_sintese.csv` |
| **H2:** setores reclassificados: automóvel / pedestre | 23 / 78 | `nb061_h2_sintese.csv` |

O treinamento da GNN não é reprodutível bit a bit entre máquinas (ver a seção seguinte). Para
reproduzir exatamente os números do relatório, use o grafo imputado do pacote do Zenodo
(`dados/intermediarios/02_grafo/zonaUrbana_5km_road_imputed.parquet`) e execute a partir do `03.1`.

## Estrutura do repositório

```
ae2sfca-ubs/
├── notebooks/            # pipeline numerado (01.1 → 06.1)
├── src/mapeprof/         # pacote reutilizável
│   ├── config.py         #   caminhos e CRS centralizados (EPSG 31983 / 4674 / 4326)
│   ├── viz.py            #   estilo cartográfico e helpers (escala, norte, moldura, eixos, zoom)
│   ├── overture.py       #   extração de atributos aninhados da Overture
│   └── geom.py           #   métricas geométricas (linearidade das arestas)
├── outputs/
│   ├── figuras/nbXYZ/    #   figuras da dissertação, por notebook
│   └── tabelas/nbXYZ/    #   tabelas da dissertação, por notebook
├── docs/
│   └── README_DATASET.md #   descrição do dataset publicado no Zenodo
├── dados/                # NÃO versionada — ver seção "Dados"
├── pyproject.toml · uv.lock · .python-version
└── LICENSE · LICENSE-DATA
```

## Método e hipóteses

A malha viária da Overture é limpa e corrigida topologicamente; lacunas de classificação
funcional são imputadas por uma Rede Neural em Grafos (GraphSAGE). A rede vira impedâncias de
tempo (fator de fricção urbana), das quais se geram isócronas por UBS nos modos automóvel e
pedestre. O índice AE2SFCA reparte a demanda dos setores **pela área** (e não pelo centroide),
corrigindo distorções nas periferias.

- **H1 (socioterritorial):** a acessibilidade às UBS não é uniforme, mas condicionada pelo
  modo de deslocamento. É testada pelo cruzamento entre o índice e a renda mediana dos setores
  (correlação de Spearman, I de Moran bivariado e LISA), separadamente por modo.
- **H2 (metodológica):** a representação areal da demanda corrige erros sistemáticos de
  classificação da abordagem tradicional por centroide (falsos desertos e falsas coberturas).
  É testada pela comparação entre o AE2SFCA e o E2SFCA (Spearman e reclassificação de desertos).

## Reprodutibilidade e limitações

- **Versões fixadas:** release da Overture, competência do CNES e versão das bibliotecas
  (`uv.lock`). Sementes: `42` (GNN, betweenness aproximada e LISA).
- **GNN:** o treinamento não é bit a bit reprodutível entre máquinas e versões de bibliotecas.
  Por isso o grafo imputado é distribuído no dataset.
- **CNES:** é um registro vivo; a competência `202604` é um retrato de abril de 2026. O pacote do
  Zenodo contém apenas a tabela de equipes (sem dados de profissionais).
- **Camadas da Prefeitura:** dependem de um geoportal que só permite visualização; a exportação
  não é reproduzível por script.
- **Setores sem dado:** 35 dos 1.375 setores urbanos não têm população/renda (18 sem linha na
  tabela do IBGE e 17 omitidos por sigilo estatístico) e são excluídos das análises.
- **Rede não direcionada:** as isócronas não consideram o sentido das vias (`oneway`); é  irrelevante a pé.

## Solução de problemas

| Sintoma | Causa provável | Solução |
|---|---|---|
| `FileNotFoundError` ao gravar em `dados/externos/…` | Pasta inexistente (Rota C) | Crie o esqueleto de pastas (seção "Rota C") |
| O `01.3` começa a baixar ~700 MB | ZIP do CNES ausente **ou com nome diferente** | Confirme `dados/externos/cnes/BASE_DE_DADOS_CNES_202604.ZIP` (com `.ZIP` maiúsculo em Linux/macOS) |
| O `01.3` não encontra a camada de UBS | Nome de arquivo diferente | Use os nomes exatos da seção "Aquisição manual" |
| `uv sync` demora | Instalação do PyTorch | Normal na primeira vez (o `uv` faz cache) |
| Falha ao baixar a Overture (`01.2`) ou o CNES (`01.3`) | Release/competência removida da fonte | Use as Rotas A ou B (o dataset contém os arquivos) |
| Notebook sem o pacote `mapeprof` | Kernel diferente do `.venv` | Selecione o interpretador `.venv` do projeto |

## Como citar

Dissertação:

```bibtex
@mastersthesis{dantas2026acessibilidade,
  title  = {Acessibilidade Geográfica às UBS de Teresina via AE2SFCA},
  author = {Dantas, Felipe Ramos},
  year   = {2026},
  school = {Instituto Federal do Piauí — MAPEPROF},
  url    = {[PREENCHER: link do repositório institucional]}
}
```

Dados:

```bibtex
@misc{dantas2026dados,
  title     = {Dataset --- Acessibilidade Geográfica às UBS de Teresina-PI (AE2SFCA)},
  author    = {Dantas, Felipe Ramos},
  year      = {2026},
  version   = {v1.0},
  publisher = {Zenodo},
  doi       = {https://doi.org/10.5281/zenodo.22964753}
}
```

Código:

```bibtex
@software{dantas2026codigo,
  title     = {ae2sfca-ubs: roteiro computacional AE2SFCA para Teresina-PI},
  author    = {Dantas, Felipe Ramos},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {[PREENCHER: DOI do código]},
  url       = {https://github.com/felipedantas-pi/ae2sfca-ubs}
}
```

## Licença

- Código: [MIT](LICENSE)
- Texto, figuras e tabelas: [CC BY 4.0](LICENSE-DATA)
- Dados de terceiros (IBGE, Overture Maps, CNES/DataSUS, Prefeitura de Teresina): mantêm as
  licenças e os termos de uso de origem, detalhados em [`docs/README_DATASET.md`](docs/README_DATASET.md).

## Sobre o programa

Pesquisa desenvolvida no **MAPEPROF** — Programa de Pós-Graduação Profissional em Análise
e Planejamento Espacial / IFPI.

- **Orientador:** Prof. Dr. Antonio Joaquim da Silva
- **Coorientador:** Prof. Dr. Reurysson Chagas de Sousa Morais
- 🌐 Site oficial: <https://www.ifpi.edu.br/mapeprof>
- 📷 Instagram: [@mapeprof](https://www.instagram.com/mapeprof/)

## Contato

Felipe Ramos Dantas — <felipe.dantas@ifpi.edu.br>
