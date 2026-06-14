"""Extração de atributos aninhados (names, surface, speed) da Overture Maps."""
import ast
import json
import numpy as np
import pandas as pd


def _coerce_aninhado(valor):
    """Normaliza o valor aninhado para dict/list, vindo de qualquer formato de arquivo.

    - GeoParquet entrega numpy.ndarray de dicts  → converte para list
    - GeoPackage/GeoJSON entregam string         → parseia com ast/json
    - Em memória já pode ser dict/list           → retorna como está
    Retorna None se ausente ou ilegível.
    """
    if valor is None:
        return None
    if isinstance(valor, np.ndarray):
        return valor.tolist() if valor.size > 0 else None
    if isinstance(valor, (dict, list)):
        return valor
    if isinstance(valor, float) and pd.isna(valor):
        return None
    if isinstance(valor, str):
        s = valor.strip()
        if not s or s.lower() in ('none', 'nan', 'null'):
            return None
        # ast.literal_eval: repr Python (aspas simples) | json.loads: JSON (aspas duplas)
        for parser in (ast.literal_eval, json.loads):
            try:
                return parser(s)
            except (ValueError, SyntaxError):
                continue
    return None


def extrair_nome_via(valor):
    """Nome primário da via. Aceita 'names' (dict) ou 'routes' (lista de dicts)."""
    obj = _coerce_aninhado(valor)

    # Caso 1: coluna 'names' → {'primary': 'Av. Frei Serafim', ...}
    if isinstance(obj, dict):
        nome = obj.get('primary')
        return nome if isinstance(nome, str) and nome.strip() else None

    # Caso 2: coluna 'routes' → [{'ref': 'BR-343'}, ...]
    if isinstance(obj, list):
        refs = []
        for item in obj:
            if isinstance(item, dict):
                ref = item.get('ref')
                if isinstance(ref, str) and ref.strip():
                    refs.append(ref.strip())   # ← corrigido (era 'appenf')
        if refs:
            return " / ".join(refs)            # ex.: 'BR-343 / PI-112'

    return None


def extrair_superficie(valor):
    """Tipo de superfície da via. Estrutura: [{'value': 'paved', ...}]. Retorna 'unknown' se ausente."""
    obj = _coerce_aninhado(valor)
    if isinstance(obj, list) and obj:
        primeiro = obj[0]
        if isinstance(primeiro, dict):
            return primeiro.get('value', 'unknown') or 'unknown'
    return 'unknown'


def extrair_velocidade_maxima(valor):
    """Maior velocidade máxima (km/h) das regras da Overture. None se ausente."""
    obj = _coerce_aninhado(valor)

    velocidades = []
    regras = obj if isinstance(obj, list) else [obj] if isinstance(obj, dict) else []
    for item in regras:
        if isinstance(item, dict) and isinstance(item.get('max_speed'), dict):
            val = item['max_speed'].get('value')
            if val is not None:
                try:
                    velocidades.append(float(val))
                except (ValueError, TypeError):
                    pass

    return max(velocidades) if velocidades else None