"""Converte os notebooks do roteiro em PDFs A4 (apêndices da dissertação).

Sem LaTeX: renderiza o HTML do nbconvert via Chromium headless (Playwright).
Contorna o bug de event loop do Playwright no Windows e força quebra de linha
no código para não vazar da página A4.

Características:
- **somente código** (saídas/figuras omitidas — `exclude_output`);
- fonte compacta (ajuste em `FONTE_PT`);
- título de apêndice no topo de cada PDF, no padrão
  "Apêndice <L>: <num> — <Título do Notebook>" (extraído do H1 do notebook).

Uso:  uv run python scripts/notebooks_to_pdf.py
Saída: dados/dissertacao/apendices_pdf/Apendice_<letra>_NB_<num>.pdf
"""
import sys
import re
import asyncio
import glob
import subprocess
from pathlib import Path

if sys.platform == "win32":  # Playwright exige ProactorEventLoop p/ subprocessos
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import nbformat
from nbconvert import HTMLExporter
from playwright.sync_api import sync_playwright

# Mapa Apêndice -> prefixo do notebook (01.4 e 01.5 não são apêndices)
APENDICES = {"A": "01.1", "B": "01.2", "C": "01.3", "D": "02.1", "E": "02.2",
             "F": "03.1", "G": "04.1", "H": "05.1", "I": "05.2", "J": "06.1"}

FONTE_PT = 10          # corpo (markdown); o código usa FONTE_PT - 1
MARGENS = {"top": "2cm", "left": "1cm", "bottom": "1cm", "right": "1cm"}
SAIDA = Path("dados/dissertacao/apendices_pdf")
SAIDA.mkdir(parents=True, exist_ok=True)

CSS = (f"<style>"
       f"@page{{size:A4;margin:{MARGENS['top']} {MARGENS['right']} {MARGENS['bottom']} {MARGENS['left']};}}"
       f"body{{font-size:{FONTE_PT}pt;}}"
       f"pre,.highlight,.highlight pre{{white-space:pre-wrap!important;"
       f"word-break:break-word;font-size:{FONTE_PT-1}pt;}}"
       f".ap-titulo{{font-family:Arial,Helvetica,sans-serif;font-size:12pt;font-weight:bold;"
       f"text-transform:uppercase;text-align:center;margin:0 0 16px 0;}}"
       f"</style>")

# omite as saídas: apêndices mostram apenas o código
html_exp = HTMLExporter(exclude_output=True)


def titulo_do_notebook(nb, pref):
    """Extrai o título a partir do H1 '# Notebook XX.X — Título'."""
    src = "".join(nb.cells[0]["source"])
    m = re.search(r"#\s*Notebook\s+[\d.]+\s*[—–-]\s*(.+)", src)
    return m.group(1).strip() if m else pref


def lancar_chromium(pw):
    """Lança o Chromium headless. Se o navegador não estiver instalado (fallback),
    instala-o automaticamente com 'playwright install chromium' e tenta de novo."""
    try:
        return pw.chromium.launch()
    except Exception:
        print("Navegador do Playwright ausente — instalando (uma vez só)...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        return pw.chromium.launch()


with sync_playwright() as pw:
    browser = lancar_chromium(pw)
    for letra, pref in APENDICES.items():
        nb_path = glob.glob(f"notebooks/{pref}_*.ipynb")[0]
        nb = nbformat.read(nb_path, as_version=4)
        titulo = titulo_do_notebook(nb, pref)

        html, _ = html_exp.from_notebook_node(nb)
        html = html.replace("</head>", CSS + "</head>")
        cabecalho = f'<h1 class="ap-titulo">Apêndice {letra}: {pref} — {titulo}</h1>'
        html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + cabecalho, html, count=1)

        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        pdf_path = SAIDA / f"Apendice_{letra}_NB_{pref}.pdf"
        try:
            page.pdf(path=str(pdf_path), print_background=True, prefer_css_page_size=True)
            print(f"  OK  Apendice {letra} ({pref}) -> {pdf_path.name}  | {titulo[:42]}")
        except PermissionError:
            print(f"  !!  Apendice {letra} ({pref}) PULADO — '{pdf_path.name}' está aberto/travado")
        page.close()
    browser.close()

print(f"\nPDFs (somente código, {FONTE_PT} pt) em: {SAIDA.resolve()}")
