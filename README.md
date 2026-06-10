# Acessibilidade Geográfica às UBS de Teresina

Aplicação do método **AE2SFCA** (Areal Enhanced 2-Step Floating Catchment Area)
para mensurar a acessibilidade geográfica às Unidades Básicas de Saúde de
Teresina-PI.

> Dissertação de Mestrado — MAPEPROF/IFPI — Felipe Ramos Dantas

## Pré-requisitos

- Python 3.11+
- `uv` ([instalação](https://docs.astral.sh/uv/))
- ~5 GB livres em disco para os dados externos

## Instalação

```bash
git clone https://github.com/felipedantas-pi/mapeprof-accessibility-ubs.git
cd mapeprof-accessibility-ubs
uv sync
```

## Dados

Os dados brutos não estão versionados no repositório. Veja
[`docs/DADOS_EXTERNOS.md`](docs/DADOS_EXTERNOS.md) para baixar
IBGE, Overture e CNES, ou rode:

```bash
uv run python scripts/baixar_dados_externos.py
```

## Executar o pipeline

Execute os notebooks em ordem:

```
notebooks/01.1 → 01.2 → 01.3 → 02.1 → 02.2 → 03.1 → 04.1 → 05.1
```

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `notebooks/` | Pipeline completo em Jupyter |
| `src/mapeprof/` | Código Python reutilizável |
| `dados/` | Dados (não versionados — ver `docs/DADOS_EXTERNOS.md`) |
| `outputs/` | Figuras e tabelas da dissertação |
| `docs/` | Documentação metodológica |

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