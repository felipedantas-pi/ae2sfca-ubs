# Contexto da Sessão — Pipeline AE2SFCA-UBS Teresina

> Documento de retomada. Resume o estado do projeto para continuar o trabalho em outra
> máquina/instância sem acesso ao histórico de conversa. Última atualização: 2026-06-15.

---

## 1. Estado Atual do Pipeline

| Notebook | Conteúdo | Status |
|---|---|---|
| `01.1` Aquisição IBGE | Limites territoriais, setores censitários | ✅ Concluído |
| `01.2` Overture | Malha viária (segment/connector) + edificações; salva **GeoJSON** | ✅ Concluído |
| `01.3` UBS/CNES | 75 UBS da zona urbana (`ubs_zonaUrbana.geojson`, coluna `cnes`) | ✅ Concluído |
| `01.4` Visualização | EDA cartográfica | ✅ Concluído |
| `02.1` Limpeza/Topologia | Filtro semântico, `process_overture_segments`, atributos, `aresta_id`, AED | ✅ Concluído |
| `02.2` Imputação GNN | GraphSAGE + baseline RF + correção de continuidade (`class_final`) | ✅ Concluído |
| `03.1` Impedâncias | Tempos multimodais (carro/pé), fricção, traversabilidade por modo | ✅ Concluído |
| `04.1` Isócronas | `concave_hull_alpha`, custo de terminal, anéis, 2 modos | ✅ Concluído |
| `05` AE2SFCA | Índice areal (carro+pé) + baseline E2SFCA + desertos | 🟡 **Criado, falta a OFERTA (S_j)** |
| `06` Testes H1/H2 | Comparação E2SFCA (H1) + Moran/LISA acesso×renda (H2) | 🔴 **Não criado** |

Árvore git limpa; tudo commitado. Saídas em `dados/intermediarios/` e `dados/processados/`
(symlink para Drive, fora do git). Figuras versionadas em `outputs/figuras/nbXXX/`.

---

## 2. Alterações e Decisões Técnicas

- **`src/mapeprof/overture.py` — `_coerce_aninhado`**: GeoParquet entrega atributos aninhados
  (`names`, `road_surface`, `speed_limits`) como `numpy.ndarray`, que o city2graph e o parser
  original não tratavam (extração retornava `unknown` para tudo). Solução: tratar `ndarray`
  (`.tolist()`) além de `str`/`dict`/`list`.

- **NB 02.1 — chave `aresta_id`**: o `id` da Overture **deixa de ser único** após o
  *connector splitting* (trechos derivados herdam o id; há ~14 ids repetidos na fonte).
  Solução: criar `aresta_id = "aresta_NNNNNN"` como chave primária. `split_from`/`split_to`
  são **frações 0–1** do segmento original, não ids de nós.

- **NB 02.2 — features e modelo**: vetor = `length_m`, `linearity`, `is_paved`, `grau`,
  `betweenness`. A **centralidade `betweenness`** (2ª feature mais preditiva) é calculada com
  `networkx` (aproximada, `k=400`, ~78 s) sobre o **grafo dual** construído por adjacência de
  extremidades. *momepy foi descartado para centralidade: `closeness`/`straightness` locais são
  lentíssimas nesta malha.*
  - **Balanceamento de classes REJEITADO**: `class_weight="balanced"` eleva F1 macro
    marginalmente mas **distorce a imputação** (residencial cai de ~66% para ~12%, infla
    `track`, rebaixa velocidade). Modelo final = **GraphSAGE sem ponderação** (F1 weighted
    ~0,66 > RF ~0,64). RF é baseline para justificar a escolha.
  - **Correção de continuidade (Seção 8 → `class_final`)**: corrige descontinuidades funcionais
    (ex.: trecho `tertiary` dentro de avenida `primary`). Critério conservador cumulativo:
    via nomeada + dirigível + ≥2 níveis abaixo da classe dominante do corredor + dominante
    cobre ≥60% da extensão + comprimento <150 m. Resultado: **133 segmentos (0,25%)**.
    `class_imputada` é preservada; correção vai para `class_final`.

- **NB 03.1 — impedâncias**: `tempo = (dist_km / vel) × 60`. Carro usa `SPEED_DICT` por
  classe × **fricção 0,70** (Campanelli). Pedestre = 4,8 km/h constante (sem fricção).
  **Traversabilidade por modo via impedância ∞** (não remove arestas): carro proibido em
  `footway/path/steps/pedestrian/cycleway`; pedestre proibido em `motorway/trunk`.
  **Ciclovia corrigida para não-dirigível** por carro. Usa `class_final`.

- **NB 04.1 — isócronas**: `c2g.utils.create_isochrone(method="concave_hull_alpha",
  hull_ratio=0.15)`. **Um grafo por modo** (descarta arestas de tempo ∞). Anéis mutuamente
  exclusivos por diferença geométrica. **Custo de terminal: 4 min só no carro (6/16/26
  efetivos); pedestre = 0** (chega à porta; usa 10/20/30 cheios).

- **NB 05 — AE2SFCA**: `gpd.overlay` (anéis × setores) → fração areal; Passo 1
  `Rⱼ = Sⱼ/demanda_ponderada`, Passo 2 `Aᵢ = Σ Rⱼ·w·frac`. Baseline E2SFCA por centroide
  (`sjoin within`) para H1. Desertos = quartil inferior. **S_j provisório = 1 por UBS.**

---

## 3. Regras de Negócio e Convenções

- **CRS**: `CRS_METRICO` = EPSG:31983 (UTM 23S, métrico); `CRS_GEOGRAFICO` = EPSG:4674;
  `CRS_WGS84` = EPSG:4326. Usar constantes de `mapeprof.config`, nunca strings cruas.
- **Caminhos** sempre via `mapeprof.config`: `INT_GRAFO`=02_grafo, `INT_IMPEDANCIAS`=04_impedancias,
  `INT_ISOCRONAS`=05_isocronas, `PROCESSADOS`, `EXT_*`. Notebooks usam o pacote `mapeprof`.
- **Nomenclatura de dados**: prefixo `zonaUrbana_5km_` (sem "Real"). Coluna de classe final
  da via = **`class_final`** (após GNN + continuidade). Chave de aresta = `aresta_id`.
- **Parâmetros do modelo**:
  - `SPEED_DICT` (km/h): motorway 80, trunk 70, primary 60, secondary 50, tertiary 40,
    residential 30, living_street 20, service 20, track 20. Vias de pedestres e ciclovia:
    não dirigível.
  - Fricção urbana (carro): **0,70**. Velocidade pedestre: **4,8 km/h**.
  - Custo de terminal: **carro 4 min, pedestre 0**. Limiares isócronas: **10/20/30 min**.
  - Pesos de decaimento AE2SFCA: **{10: 1,00; 20: 0,68; 30: 0,22}** (Luo & Qi, 2009).
  - População de demanda = `V01006_demog`. Renda = uma de `V06003`–`V06006_renda` (**confirmar qual é a média**).
- **Dependências**: `city2graph==0.3.1` (FIXADO), `torch`/`torch_geometric`, `momepy`,
  `esda`/`libpysal` (Moran/LISA). Ambiente gerido por `uv`.
- **Figuras (ABNT)**: nunca `ax.set_title()` (título vai na legenda); sempre legenda
  "Figura X – ..." + linha "Fonte: Elaborado pelo autor (2026)[, com dados de ...]".
- **Repositório GitHub**: `felipedantas-pi/ae2sfca-ubs` (hífen). Apêndices = notebooks
  inteiros (Apêndice A=01.1 ... H=05). Marcadores no texto: "(Apêndice X — Notebook YY)".

---

## 4. Pendências e Próximos Passos (prioridade)

1. **Definir a OFERTA (S_j)** — bloqueia o fechamento do NB 05. Quantificar a capacidade real
   de cada UBS (ex.: nº de equipes de Saúde da Família/eSF ou profissionais via CNES). Hoje
   está provisória (1 por UBS).
2. **Confirmar a variável de RENDA** (qual de `V06003`–`V06006_renda` é renda *média* por
   responsável, não total) — necessária para H2.
3. **Rodar o NB 05** com S_j real; gerar mapas dos índices (carro/pé) e dos desertos.
4. **Criar o NB 06** — testes estatísticos: H1 (AE2SFCA areal × E2SFCA centroide, Spearman +
   contagem de setores reclassificados) e H2 (acesso×renda, Spearman + Moran/LISA via `esda`),
   contrastando os dois modos.
5. **Dissertação**: redigir cap. Resultados (5.1 já redigível); Conclusão (esqueletos de 6.1
   Síntese e 6.4 Limitações prontos); inserir figuras do NB 05; padronizar marcadores de
   apêndice; resolver comentário [FR1] (pág. 6) e marcadores em destaque restantes.

---

## 5. Advertências e Pontos de Atenção

- ⚠️ **city2graph 0.3.1 — `concave_hull_knn` TRAVA o interpretador** (Fatal Python error no
  shapely). Usar SEMPRE `concave_hull_alpha`. **Não atualizar para 0.4.0** sem revalidar
  (pin `==0.3.1`; a dissertação cita a versão).
- ⚠️ **Balanceamento de classes na GNN distorce a imputação** — manter modelo SEM ponderação.
- ⚠️ Coluna `class` lida de parquet vem como tipo **Arrow**; o sklearn não a indexa. Converter
  com `.astype(str).to_numpy()` antes de treinar.
- ⚠️ **GeoParquet** serializa atributos aninhados como `ndarray` (incompatível com city2graph);
  por isso o NB 01.2 salva **GeoJSON** e `overture._coerce_aninhado` trata ambos os formatos.
- ⚠️ `unclassified`/`unknown`/`road` foram **imputados** (0 remanescentes em `class_final`);
  entradas mortas removidas do `SPEED_DICT`.
- ⚠️ A `velocidade_max` da Overture **não é fundida** no cálculo (só usada na figura de
  calibração); a impedância usa exclusivamente o `SPEED_DICT` × fricção.
- ⚠️ **H2 — sinal da correlação**: teste preliminar (S_j=1, renda não confirmada) deu
  correlação **positiva (~+0,49)**. Reconciliar com a hipótese "inversa": se as UBS do SUS se
  concentram em áreas de menor renda, o sinal inverso se justifica; caso contrário, revisar a
  redação da H2. **Depende de S_j e da variável de renda corretos.**
- ⚠️ NB 04 leva **~20–25 min** (75 UBS × 2 modos). Rodar uma vez e reutilizar os parquets.
- ⚠️ Classe `service` mantida como dirigível (20 km/h) por decisão documentada (condomínios
  mapeados como serviço); é uma limitação registrada.

---

## 6. Citações e Referências Relevantes

- **Michels et al. (2024)** — método areal (A2SFCA); repositório `cybergis/A2SFCA` (implementação
  de referência em GeoPandas, sem pysal). O AE2SFCA adotado = areal + *enhanced* (decaimento).
  Origem da sobreposição areal da demanda (Passo 1/2 do NB 05).
- **Luo & Qi (2009)** — E2SFCA; origem dos pesos de decaimento 1,00/0,68/0,22 e das faixas
  10/20/30 min.
- **Hacar; Altafini; Cutini (2024)** — *Network-Based Hierarchical Feature Augmentation*;
  fundamenta o uso de **centralidade de rede** como feature da GNN (centralidade > geometria).
- **Hamilton; Ying; Leskovec (2017)** — arquitetura **GraphSAGE** (NB 02.2).
- **Breiman (2001)** — **Random Forest** (baseline do NB 02.2).
- **Campanelli et al. (2026)** — fricção urbana (fator 0,70) e custo de terminal (NB 03/04).
- **Thomson (2003)** — *strokes* / princípio da boa continuação; fundamenta a correção de
  continuidade funcional (NB 02.2, Seção 8).
- **Anselin (1995); Rey & Anselin (2010)** — Moran/LISA (`esda`) para o teste de H2 (NB 06).
- **Sato (2026)** — biblioteca `city2graph`.
- **Fleischmann (2019)** — `momepy` (avaliado para centralidade, descartado por desempenho).
