"""Caminhos, CRS e constantes globais do projeto AE2SFCA-UBS."""
from pathlib import Path

# ── Raiz do projeto ───────────────────────────────────────────────────────────
# Este arquivo está em  src/mapeprof/config.py
# parents[0]=mapeprof , parents[1]=src , parents[2]=RAIZ do projeto
ROOT = Path(__file__).resolve().parents[2]

# ── Dados (a pasta 'dados' é um atalho/symlink para o Google Drive) ───────────
DADOS = ROOT / "dados"

# Entradas externas — brutas, NÃO modificar
EXTERNOS     = DADOS / "externos"
EXT_IBGE     = EXTERNOS / "ibge"
EXT_OVERTURE = EXTERNOS / "overture"
EXT_CNES     = EXTERNOS / "cnes"
EXT_PMT      = EXTERNOS / "pmt"

# Intermediários — saídas de cada etapa do pipeline (descartáveis/regeráveis)
INTERMEDIARIOS  = DADOS / "intermediarios"
INT_MALHA       = INTERMEDIARIOS / "01_malha"
INT_GRAFO       = INTERMEDIARIOS / "02_grafo"
INT_UBS         = INTERMEDIARIOS / "03_ubs"
INT_IMPEDANCIAS = INTERMEDIARIOS / "04_impedancias"
INT_ISOCRONAS   = INTERMEDIARIOS / "05_isocronas"

# Produto final do pipeline
PROCESSADOS = DADOS / "processados"

# ── Saídas versionadas no repositório ─────────────────────────────────────────
OUTPUTS = ROOT / "outputs"
FIGURAS = OUTPUTS / "figuras"
TABELAS = OUTPUTS / "tabelas"
VECTORS = OUTPUTS / "vectors"

# ── Sistemas de Referência de Coordenadas ─────────────────────────────────────
CRS_METRICO    = "EPSG:31983"   # SIRGAS 2000 / UTM 23S (metros) — distâncias e áreas
CRS_GEOGRAFICO = "EPSG:4674"    # SIRGAS 2000 geográfico (graus)
CRS_WGS84      = "EPSG:4326"    # WGS 84 — exigido pela API da Overture Maps


def criar_diretorios():
    """Cria as pastas de saída do pipeline, se ainda não existirem."""
    for d in (INT_MALHA, INT_GRAFO, INT_UBS , INT_IMPEDANCIAS, INT_ISOCRONAS,
              PROCESSADOS, FIGURAS, TABELAS, VECTORS):
        d.mkdir(parents=True, exist_ok=True)