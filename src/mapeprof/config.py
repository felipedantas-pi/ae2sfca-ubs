"""Caminhos, CRS e constantes globais do projeto."""
from pathlib import Path

# Raiz do projeto (ajustado para chamada a partir de notebooks/)
ROOT = Path(__file__).resolve().parents[2]

DADOS = ROOT / "dados"
EXTERNOS = DADOS / "externos"
INTERMEDIARIOS = DADOS / "intermediarios"
PROCESSADOS = DADOS / "processados"

OUTPUTS = ROOT / "outputs"
FIGURAS = OUTPUTS / "figuras"

# Sistemas de Referência de Coordenadas
CRS_GEOGRAFICO = "EPSG:4674"   # SIRGAS 2000
CRS_METRICO = "EPSG:31983"     # SIRGAS 2000 / UTM 23S