# Acessibilidade Geográfica às UBS de Teresina

Roteiro computacional aberto e reprodutível que aplica o método **AE2SFCA**
(*Areal Enhanced Two-Step Floating Catchment Area*) para mensurar a acessibilidade
geográfica às Unidades Básicas de Saúde (UBS) da zona urbana de Teresina-PI, nos
modos automóvel e pedestre, e diagnosticar as desigualdades socioespaciais de acesso.

> Dissertação de Mestrado — MAPEPROF/IFPI — Felipe Ramos Dantas (2026)

## Pré-requisitos

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) para gerenciamento de ambiente e dependências
- Espaço em disco para os dados externos (IBGE, Overture, CNES)

## Instalação

```bash
git clone https://github.com/felipedantas-pi/ae2sfca-ubs.git
cd ae2sfca-ubs
uv sync
```

## Dados

Os dados brutos **não são versionados**. A maior parte é adquirida automaticamente
pelos próprios notebooks via requisições HTTP às fontes oficiais — IBGE (Censo 2022 –
Agregados por Setores), Overture Maps (malha viária e edificações) e CNES/DataSUS
(equipes de Atenção Primária). A **única etapa manual** é a camada de UBS e as áreas
de atuação das equipes de Saúde da Família, exportadas da plataforma cartográfica da
Prefeitura de Teresina (SEMPLAM).

A pasta `dados/` é um *symlink* para armazenamento externo (Google Drive), organizada em
`externos/`, `intermediarios/` e `processados/`. Arquivos grandes (> 50 MB) ficam fora do
git e sincronizam pelo Drive.

## Pipeline

Execute os notebooks **em ordem** (Jupyter/Positron). Cada um corresponde a um apêndice
(A–J) da dissertação.

| Notebook | Etapa | Apêndice |
|---|---|---|
| `01.1` | Limites IBGE, setores censitários e demanda (censo) | A |
| `01.2` | Malha viária e edificações (Overture Maps) | B |
| `01.3` | UBS e capacidade instalada (CNES) | C |
| `01.4` | Visualização cartográfica | — |
| `01.5` | Análise exploratória socioeconômica | — |
| `02.1` | Limpeza e correção topológica da malha | D |
| `02.2` | Imputação de classes funcionais por Rede Neural em Grafos | E |
| `03.1` | Definição de velocidades e cálculo de impedâncias | F |
| `04.1` | Geração das isócronas (10/20/30 min) | G |
| `05.1` | Cálculo do índice de acessibilidade AE2SFCA | H |
| `05.2` | Teste de robustez dasimétrica da demanda | I |
| `06.1` | Testes das hipóteses (H1 metodológica e H2 territorial) | J |

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `notebooks/` | Pipeline numerado (Jupyter) |
| `src/mapeprof/` | Pacote Python reutilizável |
| `src/mapeprof/config.py` | Caminhos e CRS centralizados (EPSG 31983 / 4674 / 4326) |
| `src/mapeprof/viz.py` | Estilo cartográfico e *helpers* de mapa (escala, norte, moldura, eixos, zoom) |
| `src/mapeprof/overture.py` | Extração de atributos aninhados da Overture |
| `src/mapeprof/geom.py` | Métricas geométricas (linearidade das arestas) |
| `dados/` | Dados (não versionados — *symlink* externo) |
| `outputs/figuras/` · `outputs/tabelas/` | Figuras e tabelas da dissertação, por notebook (`nbXYZ/`) |

## Método (resumo)

A malha viária da Overture é limpa e corrigida topologicamente; lacunas de classificação
funcional são imputadas por uma Rede Neural em Grafos. A rede vira impedâncias de tempo
(fator de fricção urbana), das quais se geram isócronas por UBS nos modos automóvel e
pedestre. O índice AE2SFCA reparte a demanda dos setores **pela área** (e não pelo
centroide), corrigindo distorções nas periferias. O diagnóstico é confrontado com o
E2SFCA tradicional (H1) e com a renda mediana domiciliar, via correlação de Spearman e
autocorrelação espacial (I de Moran e LISA) (H2); um teste dasimétrico verifica a robustez
ao MAUP.

## Citação

```bibtex
@mastersthesis{dantas2026acessibilidade,
  title  = {Acessibilidade Geográfica às UBS de Teresina via AE2SFCA},
  author = {Dantas, Felipe Ramos},
  year   = {2026},
  school = {Instituto Federal do Piauí — MAPEPROF}
}
```

## Licença

- Código: [MIT](LICENSE)
- Texto, figuras e tabelas: [CC BY 4.0](LICENSE-DATA)
