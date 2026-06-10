"""Helpers de geometria para os segmentos viários."""
from shapely.geometry import Point


def calcular_linearidade(geom):
    """Razão entre a distância reta (ponta a ponta) e o comprimento da via. [0,1]; 1 = reta perfeita."""
    try:
        d_euclidiana = Point(geom.coords[0]).distance(Point(geom.coords[-1]))
        return d_euclidiana / geom.length if geom.length > 0 else 0.0
    except Exception:
        return 0.0