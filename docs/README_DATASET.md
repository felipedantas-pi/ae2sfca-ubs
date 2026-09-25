# Dataset — Acessibilidade Geográfica às UBS de Teresina-PI (AE2SFCA)

**Versão:** v1.0 · **DOI:** [https://doi.org/10.5281/zenodo.22964753](https://doi.org/10.5281/zenodo.22964753) · **Data de publicação:** [PREENCHER: dd/mm/aaaa] · **Licença:** ver seção 9

Dados de entrada, intermediários e derivados do roteiro computacional que aplica o método
**AE2SFCA** (*Areal Enhanced Two-Step Floating Catchment Area*) à acessibilidade geográfica às
Unidades Básicas de Saúde (UBS) da zona urbana de Teresina-PI, nos modos automóvel e pedestre.
Acompanha a dissertação de mestrado de Felipe Ramos Dantas (MAPEPROF/IFPI, 2026; orientador:
Prof. Dr. Antonio Joaquim da Silva; coorientador: Prof. Dr. Reurysson Chagas de Sousa Morais).

- **Código:** <https://github.com/felipedantas-pi/ae2sfca-ubs> (DOI do código: [PREENCHER: 10.5281/zenodo.YYYYYYY])
- **Dissertação:** [PREENCHER: link do repositório institucional do IFPI]

## 1. Conteúdo do registro

| Arquivo | Descrição | Tamanho |
|---|---|---|
| `ae2sfca-ubs_dados_v1.0.zip` | Pasta `dados/` completa (19 arquivos; ver seção 5) | [PREENCHER: MB do ZIP] (~100 MB descompactado) |
| `MANIFEST.csv` | Cada arquivo do ZIP com tamanho, SHA-256, origem e licença | < 1 MB |
| `README_DATASET.md` | Este documento | — |

O ZIP contém a pasta `dados/` na raiz. Extraído na **raiz do repositório de código**, ele recria a
estrutura que os notebooks esperam:

```
dados/
├── README.md
├── externos/
│   ├── pmt/        ubs.geojson · area_das_esf.geojson · area_das_ubs.geojson
│   ├── cnes/       BASE_DE_DADOS_CNES_202604.ZIP  (reduzido: só tbEquipe202604.csv)
│   ├── ibge/       teresina_municipio · teresina_zonaUrbana_utm · teresina_zonaUrbana_buffer5kClip_utm  (.parquet)
│   └── overture/   zonaUrbana_5km_segmentos · zonaUrbana_5km_conectores  (.geojson e .parquet)
├── intermediarios/
│   ├── 01_malha/   teresina_setoresCensitarios_DadosCompletos.parquet
│   ├── 02_grafo/   zonaUrbana_5km_road_cleaned.parquet · zonaUrbana_5km_road_imputed.parquet
│   ├── 03_ubs/     teresina_zonaUrbana_buffer5km_ubs_capacidade.parquet
│   ├── 04_impedancias/  zonaUrbana_5km_road_routed.parquet
│   └── 05_isocronas/    zonaUrbana_5km_isocronas_carro.parquet · zonaUrbana_5km_isocronas_pedestre.parquet
└── processados/    teresina_setores_acessibilidade.parquet
```

## 2. Como usar

1. Clonar o repositório de código e instalar o ambiente (`uv sync`; ver o `README.md` do repositório).
2. Baixar o ZIP deste registro para a raiz do repositório e extrair.

   **Windows (PowerShell)**

   ```powershell
   Expand-Archive -Path .\ae2sfca-ubs_dados_v1.0.zip -DestinationPath .
   ```

   **Linux / macOS**

   ```bash
   unzip ae2sfca-ubs_dados_v1.0.zip
   ```

3. (Opcional) Conferir a integridade: `Get-FileHash -Algorithm SHA256 <arquivo>` (PowerShell) ou
   `sha256sum <arquivo>` (Linux/macOS), comparando com a coluna `sha256` do `MANIFEST.csv`.

Duas rotas de uso, ambas offline:

| Rota | Notebooks a executar | Reproduz |
|---|---|---|
| **A: rápida** | `05.1` e `06.1` | O índice AE2SFCA/E2SFCA e os testes das hipóteses H1 e H2, sem repetir malha e isócronas em vez de  |
| **B: completa** | `01.3` → `06.1` (`01.4` e `01.5` opcionais) | Todo o processamento a partir das entradas. Os notebooks `01.1` e `01.2`, que baixam dados do IBGE e da Overture, podem ser pulados: suas saídas já estão no pacote |

**Por que os intermediários estão incluídos.** O treinamento da Rede Neural em Grafos (notebook `02.2`)
usa semente fixa (`42`), mas não é reprodutível bit a bit entre máquinas e versões de bibliotecas.
O grafo imputado (`zonaUrbana_5km_road_imputed.parquet`) garante os mesmos resultados da
dissertação; execute a partir do `03.1` para reproduzi-los exatamente.

**Sobre o ZIP do CNES.** O notebook `01.3` verifica a existência de
`dados/externos/cnes/BASE_DE_DADOS_CNES_202604.ZIP` (extensão `.ZIP` em maiúsculas, relevante em
Linux/macOS) e, se ausente, baixa os ~700 MB do DataSUS. O ZIP deste pacote contém apenas o arquivo
`tbEquipe202604.csv`, com o mesmo nome do original, para que o notebook funcione sem alteração.

## 3. Fontes e versões fixadas

| Origem | Versão / data | Observação |
|---|---|---|
| IBGE: malhas territoriais e Censo Demográfico 2022 | Malha de setores CD2022; agregados por setor (população `V01006`; renda do responsável `V06004`/`V06006`, arquivo `..._20260508_csv.zip`) | Setores sem dado por sigilo estatístico (`X`) ou sem linha na tabela ficam `NaN` |
| Overture Maps Foundation | Release `2026-06-17.0` | Temas `segment` (segmentos) e `connector` (conectores) |
| CNES/DataSUS | Competência `202604` | Tabela `tbEquipe`. O notebook filtra equipes tipos 70 (eAP) e 71 (eSF), ativas, do município 221100. **Dados de profissionais não foram incluídos** |
| Prefeitura de Teresina / SEMPLAN (TeresinaGeo) | Exportação manual em [PREENCHER: dd/mm/aaaa] | UBS, áreas de atuação das ESF e áreas das UBS, convertidas de KML para GeoJSON |

**Sistema de referência.** Arquivos derivados: **SIRGAS 2000 / UTM 23 Sul (EPSG:31983)**. Os
GeoJSON da SEMPLAN estão em EPSG:4326 (WGS 84) e são reprojetados pelos notebooks.

## 4. Unidades e convenções

- **Índice de acessibilidade** (`acess_carro`, `acess_pe`, `acess_*_e2sfca`): **equipes de Atenção
  Primária por habitante**. Multiplique por 10.000 para obter equipes por 10 mil habitantes, a unidade
  usada na dissertação.
- **Faixas de tempo** (`threshold_nominal`): 10, 20 e 30 minutos, em anéis mutuamente exclusivos
  (0–10, 10–20 e 20–30). No automóvel há custo de terminal de 4 minutos (`threshold` = 6, 16, 26 min efetivos).
- **Pesos de decaimento gaussiano:** 1,00 / 0,68 / 0,22 para as três faixas.
- **"Deserto de saúde":** absoluto (`acesso = 0`) ou relativo (quartil inferior entre os setores com acesso positivo).
- **Codificação:** GeoJSON e demais textos em UTF-8. A exceção é `tbEquipe202604.csv` (dentro do ZIP do CNES), em **Latin-1**, exatamente como distribuído pelo DataSUS; o notebook `01.3` o lê com `encoding="latin-1"`.

## 5. Dicionário de arquivos

### `externos/pmt/` — Prefeitura de Teresina / SEMPLAN
| Arquivo | Descrição | Usado em |
|---|---|---|
| `ubs.geojson` | 93 UBS do município (pontos, EPSG:4326), com o código CNES | 01.3 |
| `area_das_esf.geojson` | 240 áreas de atuação das equipes de Saúde da Família (polígonos), com `cnes`, `esf`, `nm_equipe`, `ine` | 01.3 |
| `area_das_ubs.geojson` | 75 áreas de atuação das UBS, com `cnes` e o atributo `regional` (SUL, NORTE, LESTE, SUDESTE) | 01.3 |

### `externos/cnes/` — CNES/DataSUS
| Arquivo | Descrição | Usado em |
|---|---|---|
| `BASE_DE_DADOS_CNES_202604.ZIP` | ZIP **reduzido**, contendo só `tbEquipe202604.csv` (equipes de saúde, competência 202604) | 01.3 |

### `externos/ibge/` — IBGE (saídas do notebook 01.1)
| Arquivo | Descrição | Usado em |
|---|---|---|
| `teresina_municipio.parquet` | Limite municipal | 01.4 |
| `teresina_zonaUrbana_utm.parquet` | Zona urbana: 1.375 setores censitários contíguos, dissolvidos em um polígono | 01.2 a 06.1 |
| `teresina_zonaUrbana_buffer5kClip_utm.parquet` | Área de estudo: zona urbana + *buffer* de 5 km, recortada ao limite municipal | 01.2 a 05.1 |

### `externos/overture/` — Overture Maps (saídas do notebook 01.2)
| Arquivo | Descrição | Usado em |
|---|---|---|
| `zonaUrbana_5km_segmentos.geojson` / `.parquet` | Segmentos viários da área de estudo (`subtype` = `road` ou `rail`), com atributos aninhados da Overture | 02.1 / 01.4 |
| `zonaUrbana_5km_conectores.geojson` / `.parquet` | Conectores (interseções) da área de estudo | 02.1 / 01.4 |

### `intermediarios/` e `processados/` — saídas do pipeline
| Arquivo | Descrição | Produzido → usado em |
|---|---|---|
| `01_malha/teresina_setoresCensitarios_DadosCompletos.parquet` | 1.375 setores com atributos do IBGE mais `populacao` (V01006), `renda_media` (V06004) e `renda_mediana` (V06006). `NaN` = sem dado (35 setores) | 01.1 → 01.3 a 06.1 |
| `03_ubs/teresina_zonaUrbana_buffer5km_ubs_capacidade.parquet` | 81 UBS da área de estudo (75 na zona urbana, 6 de borda), com `cnes`, `capacidade_equipes`, `n_esf`, `n_eap`, `regional`, `na_zona_urbana` | 01.3 → 01.4, 01.5, 04.1, 05.1 |
| `02_grafo/zonaUrbana_5km_road_cleaned.parquet` | Malha viária limpa e corrigida topologicamente (52.977 arestas) | 02.1 → 02.2 |
| `02_grafo/zonaUrbana_5km_road_imputed.parquet` | Malha com classes funcionais imputadas pela GNN (`class_imputada`) e corrigidas por continuidade (`class_final`) | 02.2 → 03.1 |
| `04_impedancias/zonaUrbana_5km_road_routed.parquet` | Malha com o tempo de travessia por aresta: `tempo_carro_min` e `tempo_pe_min` (`inf` = via proibida ao modo) | 03.1 → 04.1 |
| `05_isocronas/zonaUrbana_5km_isocronas_{carro,pedestre}.parquet` | Isócronas por UBS em anéis exclusivos: `ubs_id` (CNES), `modo`, `threshold`, `threshold_nominal`, geometria | 04.1 → 05.1 |
| `processados/teresina_setores_acessibilidade.parquet` | Por setor: `populacao`, `acess_carro`, `acess_pe` (AE2SFCA), `acess_carro_e2sfca`, `acess_pe_e2sfca` (E2SFCA), e indicadores de "deserto" (`deserto_*`, `deserto_*_abs`, `deserto_*_rel`, `deserto_*_e2sfca`) | 05.1 → 06.1 |

## 6. Limitações conhecidas

- A base CNES é um registro vivo: a competência `202604` é um retrato de abril de 2026.
- As camadas da SEMPLAN dependem de um geoportal que só permite visualização; a exportação não é
  reproduzível por script.
- 35 dos 1.375 setores urbanos não têm dado de população/renda (18 sem linha na tabela do IBGE e 17
  com valor omitido por sigilo estatístico) e são excluídos das análises.
- As isócronas usam a rede viária sem considerar o sentido das vias (`oneway`).
- O treinamento da GNN não é reprodutível bit a bit entre ambientes (ver seção 2).

## 7. Como verificar a replicação

Após executar os notebooks, os valores abaixo devem coincidir com os da dissertação:

| Grandeza | Valor |
|---|---|
| Índice médio, automóvel / pedestre (equipes por 10 mil hab.) | 5,85 / 5,62 |
| Setores em "deserto de saúde", automóvel / pedestre | 344 / 358 |
| Spearman acesso × renda mediana (H1), automóvel / pedestre | +0,438 / −0,199 |
| Spearman AE2SFCA × E2SFCA (H2), automóvel / pedestre | 0,991 / 0,949 |

## 8. Histórico de versões

| Versão | Data | Alterações |
|---|---|---|
| v1.0 | [PREENCHER: dd/mm/aaaa] | Publicação inicial |

## 9. Licenças

Este registro reúne dados de origens distintas. **Cada origem mantém sua licença e seus termos de
uso**, indicados por arquivo no `MANIFEST.csv`.

| Origem | Licença / termos |
|---|---|
| IBGE | [PREENCHER: conferir e citar os termos de uso vigentes] |
| Overture Maps Foundation | [PREENCHER: conferir a licença dos temas `segment` e `connector` na página da release 2026-06-17.0] |
| CNES/DataSUS | [PREENCHER: dados abertos; conferir e citar os termos] |
| Prefeitura de Teresina / SEMPLAN | [PREENCHER: autorização de redistribuição] |
| Produtos derivados e demais conteúdos autorais | [PREENCHER: ex. CC BY 4.0] |

## 10. Como citar

> Dantas, F. R. (2026). *Dataset — Acessibilidade Geográfica às UBS de Teresina-PI (AE2SFCA)* (v1.0)
> [Conjunto de dados]. Zenodo. https://doi.org/10.5281/zenodo.22964753

Cite também a dissertação e o código (DOI do código: [PREENCHER: 10.5281/zenodo.YYYYYYY]).

## 11. Contato

Felipe Ramos Dantas — felipe.dantas@ifpi.edu.br — MAPEPROF/IFPI
