#!/usr/bin/env python3
"""Gera o template do Elementor a partir do index.html.

Uma seção da página vira um widget HTML do Elementor, cada um dentro do seu
container de largura total. O CSS e as fontes vão no primeiro widget. Assim o
cliente reordena ou esconde seções pelo Elementor sem mexer em código, e o
desenho não depende do tema nem dos widgets padrão.

Uso: python3 exportar_elementor.py [URL base dos assets]
Sem argumento, os assets apontam para o preview no GitHub Pages.
"""
import json, re, sys, uuid, pathlib

RAIZ = pathlib.Path(__file__).parent
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://manualdotrafego.github.io/dbout-site").rstrip("/")

html = (RAIZ / "index.html").read_text(encoding="utf-8")
css = "\n".join((RAIZ / n).read_text(encoding="utf-8") for n in ("tokens.css", "base.css", "styles.css"))
css = re.sub(r'@import url\("\./[a-z]+\.css"\);\n?', "", css)
css = re.sub(r"/\* Hallmark[^\n]*\n(?: \*[^\n]*\n)*", "", css)  # os carimbos do build não precisam ir para o WordPress

def absoluto(s: str) -> str:
    return re.sub(r'(src|srcset|href|poster)="assets/', lambda m: f'{m.group(1)}="{BASE}/assets/', s)

def em_srcset(s: str) -> str:
    # só os candidatos ainda relativos (o absoluto() já trocou o primeiro)
    return re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="' + re.sub(r'(^|[\s,])assets/', lambda k: k.group(1) + f"{BASE}/assets/", m.group(1)) + '"', s)

html = em_srcset(absoluto(html))

# pedaços da página, na ordem
def pega(ini: str, fim: str) -> str:
    a = html.index(ini); b = html.index(fim, a) + len(fim)
    return html[a:b]

cabeca = pega('<a class="skip"', "</div>\n\n<main")[: -len("\n\n<main")]
secoes = re.findall(r"(<section[\s\S]*?</section>)", html)
rodape = pega('<footer class="foot">', "</footer>")
script = pega("<script>\n(() => {", "</script>")
ld = pega('<script type="application/ld+json">', "</script>")

fontes = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@700&family=Instrument+Sans:wght@400;500&display=swap" rel="stylesheet">'
estilo = f"<style>\n{css}\n/* Elementor: o tema não deve colocar margem nem fundo no conteúdo */\nhtml body, html body.elementor-page {{ background: var(--color-paper) !important; color: var(--color-ink); }}\n.elementor-section-wrap, .e-con, .e-con-inner {{ max-width: none; padding: 0; }}\n.e-con > .elementor-widget-html {{ width: 100%; }}\n.elementor-widget-html .elementor-widget-container {{ display: contents; }}\n/* o kit do Elementor e o tema pintam button e a:hover; os controles e botões da página mandam */\nbody .elementor-widget-html .btn, body .elementor-widget-html .btn:focus, body .elementor-widget-html .btn:active {{ background: var(--color-paper); color: var(--color-ink); border: 0; }}\nbody .elementor-widget-html .btn:hover {{ background: var(--color-paper-2); color: var(--color-ink); border: 0; }}\nbody .elementor-widget-html .btn--primary, body .elementor-widget-html .btn--primary:focus, body .elementor-widget-html .btn--primary:active {{ background: var(--color-accent); color: var(--color-accent-ink); }}\nbody .elementor-widget-html .btn--primary:hover {{ background: var(--color-accent-deep); color: var(--color-accent-ink); }}\nbody .elementor-widget-html .filme__ctl, body .elementor-widget-html .filme__ctl:hover, body .elementor-widget-html .filme__ctl:focus, body .elementor-widget-html .filme__ctl:active {{ background: var(--color-paper); color: var(--color-ink); border: 1px solid color-mix(in oklab, var(--color-ink) 12%, transparent); }}\nbody .elementor-widget-html a:hover {{ color: inherit; }}\n</style>"

blocos = [("Fontes, CSS e cabeçalho", fontes + estilo + '<script>document.documentElement.classList.add("js");</script>' + cabeca)]
nomes = ["Hero", "O trabalho em quatro frentes", "A jornada (filme)", "O diagnóstico", "Depoimentos e clientes", "Frase do fundador", "História e escritório", "Comece pelo diagnóstico"]
assert len(secoes) == len(nomes), f"{len(secoes)} seções no HTML, {len(nomes)} nomes: atualize a lista"
# no WordPress não existe o <main id="principal">: o hero vira o alvo do link de pular
secoes[0] = secoes[0].replace("<section ", '<section id="principal" tabindex="-1" ', 1)
for nome, sec in zip(nomes, secoes):
    blocos.append((nome, sec))
blocos.append(("Rodapé, dados estruturados e script", rodape + ld + script))

def uid() -> str:
    return uuid.uuid4().hex[:7]

def container(nome: str, conteudo: str) -> dict:
    return {
        "id": uid(), "elType": "container",
        "settings": {"content_width": "full", "flex_direction": "column", "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
                     "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}, "_title": nome},
        "elements": [{"id": uid(), "elType": "widget", "widgetType": "html", "settings": {"html": conteudo, "_title": nome}, "elements": []}],
        "isInner": False,
    }

template = {
    "version": "0.4",
    "title": "Dbout Mídia, página inicial (rebranding)",
    "type": "page",
    "page_settings": {"hide_title": "yes", "template": "elementor_canvas"},
    "content": [container(n, c) for n, c in blocos],
}
saida = RAIZ / "elementor-dbout-home.json"
saida.write_text(json.dumps(template, ensure_ascii=False), encoding="utf-8")
print(f"{saida.name}: {len(blocos)} widgets, {saida.stat().st_size // 1024} kB, assets em {BASE}/assets/")
