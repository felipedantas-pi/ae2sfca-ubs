"""Estilo visual e helpers cartográficos das figuras da dissertação."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Paletas de cores reaproveitadas pelos mapas temáticos
CORES_GROUP = {
    'Pavimentada'     : '#2166AC',
    'Não pavimentada' : '#B35806',
    'Desconhecida'    : '#CCCCCC',
}
CORES_SURF = {
    'paved': '#2166AC', 'unpaved': '#B35806', 'gravel': '#D9A641',
    'dirt': '#8C510A', 'paving_stones': '#74ADD1', 'unknown': '#AAAAAA',
}


def aplicar_estilo():
    """Aplica o estilo padrão das figuras a toda a sessão. Chamar uma vez por notebook."""
    plt.rcParams.update({
        'figure.dpi': 150, 'savefig.dpi': 300,
        'font.family': 'serif', 'font.size': 10,
        'axes.titlesize': 10, 'axes.labelsize': 10,
        'xtick.labelsize': 8, 'ytick.labelsize': 8,
        'figure.facecolor': 'white', 'axes.facecolor': '#F8F8F8',
        'axes.grid': True, 'grid.alpha': 0.4, 'grid.linestyle': '--',
        'legend.fontsize': 6, 'legend.title_fontsize': 8, 'legend.labelspacing': 1.2,
        'legend.handletextpad': 0.8, 'legend.borderpad': 0.8
    })


def barra_escala(ax, comprimento_m=5000, rotulo='5 km', frac_x=0.02, frac_y=0.01):
    """Desenha uma barra de escala métrica (UTM). Chamar DEPOIS dos .plot()."""
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    xi = x0 + (x1 - x0) * frac_x; yi = y0 + (y1 - y0) * frac_y
    h = (y1 - y0) * 0.006
    ax.add_patch(Rectangle((xi, yi), comprimento_m / 2, h, fc='black', ec='black', zorder=10))
    ax.add_patch(Rectangle((xi + comprimento_m / 2, yi), comprimento_m / 2, h, fc='white', ec='black', zorder=10))
    ax.text(xi, yi + h * 2.2, '0', ha='center', fontsize=7, zorder=10)
    ax.text(xi + comprimento_m, yi + h * 2.2, rotulo, ha='center', fontsize=7, zorder=10)


def seta_norte(ax, frac_x=0.94, frac_y=0.88):
    """Desenha uma seta de Norte. Chamar DEPOIS dos .plot()."""
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    xn = x0 + (x1 - x0) * frac_x; yn = y0 + (y1 - y0) * frac_y
    d = (y1 - y0) * 0.05
    ax.annotate('', xy=(xn, yn + d), xytext=(xn, yn),
                arrowprops=dict(arrowstyle='-|>', color='black', lw=1.6), zorder=10)
    ax.text(xn, yn + d * 1.2, 'N', ha='center', va='bottom',
            fontsize=11, fontweight='bold', zorder=10)


def moldura_mapa(ax, titulo, fonte):
    """Aplica título, rótulos de eixo (UTM) e nota de fonte a um mapa."""
    ax.set_title(titulo, pad=10)
    ax.set_xlabel('Este (m)')
    ax.set_ylabel('Norte (m)')
    ax.tick_params(labelsize=5)
    ax.figure.text(0.5, 0.005, f'Fonte: {fonte}', ha='center', fontsize=7,
                   style='italic', color='#555555')

def formatar_eixos_mapa(ax, fontsize=8):
    """
    Formata os eixos do mapa cartográfico: remove notação científica, 
    rotaciona a latitude para vertical e ajusta os tamanhos das fontes.
    """
    # 1. Remove notação científica (o '1e6') forçando formato texto
    ax.ticklabel_format(style='plain', useOffset=False)

    # 2. Rotaciona a latitude (Eixo Y) para vertical e ajusta alinhamento
    for label in ax.get_yticklabels():
        label.set_rotation(90)
        label.set_verticalalignment('center')
        label.set_fontsize(fontsize)

    # 3. Ajusta o tamanho da fonte da longitude (Eixo X)
    for label in ax.get_xticklabels():
        label.set_fontsize(fontsize)

    # 4. Define os rótulos de coordenadas métricas
    ax.set_xlabel("Este (m)", fontsize=fontsize)
    ax.set_ylabel("Norte (m)", fontsize=fontsize)


def ajustar_zoom_camada(ax, gdf_alvo, margem=0.02):
    """
    Ajusta os limites da câmera (xlim, ylim) do Matplotlib para focar estritamente 
    na caixa delimitadora (bounding box) da camada alvo, eliminando espaços em branco.
    """
    # Captura as coordenadas extremas do GeoDataFrame
    minx, miny, maxx, maxy = gdf_alvo.total_bounds
    
    # Calcula um pequeno respiro (buffer) percentual para a borda não colar no quadro
    margem_x = (maxx - minx) * margem
    margem_y = (maxy - miny) * margem

    # Aplica o recorte dinâmico
    ax.set_xlim(minx - margem_x, maxx + margem_x)
    ax.set_ylim(miny - margem_y, maxy + margem_y)