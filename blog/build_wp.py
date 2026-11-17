"""Monta o HTML de um post para o WordPress a partir do HTML renderizado pelo blog_render.py.

uso: python3 build_wp.py <html renderizado> <saida.wp.html>

O estilo vem do modelo de post do blog (blog.css, no modelo single 1053 do Elementor);
aqui sai só a marcação, dentro de um bloco wp:html.

Opcional: um arquivo <saida sem .wp.html>.sumario.json ao lado da saída, com
{"id-do-h2": "Rótulo curto"}, encurta os links do sumário (quando o post tem sumário).
"""
import html as html_lib
import json
import re
import sys
from pathlib import Path

src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()
a, b = '<!--bs-body:start-->', '<!--bs-body:end-->'
body = h[h.index(a) + len(a):h.index(b)].strip()
assert '<h1' not in body and '<script' not in body

m_alt = re.search(r'<meta property="og:image:alt" content="([^"]*)"', h)
alt_capa = html_lib.unescape(m_alt.group(1)) if m_alt else ''
assert alt_capa, 'falta og_image_alt no frontmatter'

body = body.replace('aria-label="Table"', 'aria-label="Tabela"')

# gráficos: a fonte fica só na legenda (com link), não repetida dentro do gráfico
body = re.sub(r'\s*<text[^>]*>\s*Fonte:[^<]*</text>', '', body)

# sumário (quando existe) vira <nav>, com rótulos curtos se houver o arquivo .sumario.json
m = re.search(r'<p><strong>Neste artigo:</strong></p>\s*(<ul>.*?</ul>)', body, re.S)
if m:
    lista = m.group(1)
    arq = Path(re.sub(r'\.wp\.html$', '', out) + '.sumario.json')
    if arq.exists():
        curtos = json.loads(arq.read_text(encoding='utf-8'))

        def curto(mm):
            return '<a href="#%s">%s</a>' % (mm.group(1), curtos.get(mm.group(1), mm.group(2)))
        lista = re.sub(r'<a href="#([a-z0-9-]+)">(.*?)</a>', curto, lista)
    body = (body[:m.start()] + '<nav class="sumario" aria-label="Neste artigo">\n<p class="sumario__t">Neste artigo</p>\n'
            + lista + '\n</nav>' + body[m.end():])


# aspas tipográficas só nos nós de texto
def aspas(texto):
    abre = True
    saida = []
    for ch in texto:
        if ch == '"':
            saida.append('“' if abre else '”')
            abre = not abre
        else:
            saida.append(ch)
    return ''.join(saida)


partes = re.split(r'(<[^>]+>)', body)
body = ''.join(x if x.startswith('<') else aspas(x.replace('&quot;', '"')) for x in partes)


# cada célula leva o nome da coluna, para as tabelas empilharem no celular
def rotula(mt):
    tab = mt.group(0)
    heads = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<th[^>]*>(.*?)</th>', tab, re.S)]

    def linha(ml):
        cels = re.findall(r'<td[^>]*>.*?</td>', ml.group(0), re.S)
        novo = ml.group(0)
        for i, c in enumerate(cels):
            if i == 0 or i >= len(heads):
                continue
            novo = novo.replace(c, c.replace('<td', '<td data-label="%s"' % heads[i].replace('"', ''), 1), 1)
        return novo
    return re.sub(r'<tr>\s*<td.*?</tr>', linha, tab, flags=re.S)


body = re.sub(r'<table.*?</table>', rotula, body, flags=re.S)

# a primeira citação em bloco é a caixa de principais pontos
if '<blockquote>' in body:
    body = body.replace('<blockquote>', '<blockquote class="pontos">', 1)

capa = ('<img class="capa" src="{{HERO_URL}}" width="1200" height="630" alt="%s" fetchpriority="high" decoding="async">'
        % html_lib.escape(alt_capa, quote=True))
wp = '<!-- wp:html -->\n<article id="dbout-artigo">\n' + capa + '\n' + body + '\n</article>\n<!-- /wp:html -->\n'
assert '—' not in wp and '–' not in wp
open(out, 'w', encoding='utf-8').write(wp)
print('bytes', len(wp), '| h2', wp.count('<h2'), '| tabelas', wp.count('<table'), '| svg', wp.count('<svg'),
      '| sumário', 'sim' if m else 'não')
