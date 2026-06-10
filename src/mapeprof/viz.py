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
        'axes.titlesize': 11, 'axes.labelsize': 10,
        'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 9,
        'figure.facecolor': 'white', 'axes.facecolor': '#F8F8F8',
        'axes.grid': True, 'grid.alpha': 0.4, 'grid.linestyle': '--',
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
    ax.set_title(titulo, pad=12)
    ax.set_xlabel('Este (m) — SIRGAS 2000 / UTM 23S')
    ax.set_ylabel('Norte (m) — SIRGAS 2000 / UTM 23S')
    ax.tick_params(labelsize=7)
    ax.figure.text(0.5, 0.005, f'Fonte: {fonte}', ha='center', fontsize=7,
                   style='italic', color='#555555')