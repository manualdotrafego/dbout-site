"""Monta o HTML do post para o WordPress na identidade do site (tema Dose).
uso: build_wp.py <html renderizado> <saida.wp.html>
O estilo vem do modelo de post do blog (blog.css); aqui sai só a marcação.
"""
import re, sys
src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()
a, b = '<!--bs-body:start-->', '<!--bs-body:end-->'
body = h[h.index(a) + len(a):h.index(b)].strip()
assert '<h1' not in body and '<script' not in body

# gráficos: acessibilidade preservada, largura controlada pelo CSS
assert body.count('role="img"') == 3
body = body.replace('aria-label="Table"', 'aria-label="Tabela"')

# a fonte fica só na legenda (com link), não repetida dentro do gráfico
n_f = len(re.findall(r'<text[^>]*>\s*Fonte:[^<]*</text>', body))
assert n_f == 3, n_f
body = re.sub(r'\s*<text[^>]*>\s*Fonte:[^<]*</text>', '', body)

# sumário vira <nav>
m = re.search(r'<p><strong>Neste artigo:</strong></p>\s*(<ul>.*?</ul>)', body, re.S)
assert m, 'sumário não encontrado'
body = body[:m.start()] + '<nav class="sumario" aria-label="Neste artigo">\n<p class="sumario__t">Neste artigo</p>\n' + m.group(1) + '\n</nav>' + body[m.end():]

# rótulos curtos no sumário
CURTOS = {
    'o-mercado-odontologico-no-brasil-em-numeros': 'O mercado em números',
    'anuncios-pagos-meta-ads-e-google-ads-para-clinica-odontologica': 'Anúncios pagos',
    'do-lead-ao-paciente-resposta-whatsapp-agendamento-e-lembrete': 'Do lead ao paciente',
    'a-base-de-captacao-perfil-no-google-avaliacoes-e-pagina-no-celular': 'Base de captação',
    'o-que-o-cfo-permite-e-proibe-na-publicidade-odontologica': 'Regras do CFO',
    'lgpd-no-formulario-de-captacao': 'LGPD no formulário',
    'as-metricas-que-importam': 'Métricas',
    'plano-de-90-dias': 'Plano de 90 dias',
    'perguntas-frequentes': 'Perguntas frequentes',
    'conclusao': 'Conclusão',
    'sobre-o-autor-e-este-guia': 'Autor e método',
    'fontes': 'Fontes',
}
def curto(m):
    assert m.group(1) in CURTOS, m.group(1)
    return '<a href="#%s">%s</a>' % (m.group(1), CURTOS[m.group(1)])
ini = body.index('<nav class="sumario"'); fim = body.index('</nav>', ini)
body = body[:ini] + re.sub(r'<a href="#([a-z0-9-]+)">.*?</a>', curto, body[ini:fim]) + body[fim:]

# aspas tipográficas só nos nós de texto
def aspas(texto):
    abre = True
    saida = []
    for ch in texto:
        if ch == '"':
            saida.append('\u201c' if abre else '\u201d'); abre = not abre
        else:
            saida.append(ch)
    return ''.join(saida)
partes = re.split(r'(<[^>]+>)', body)
partes = [x if x.startswith('<') else aspas(x.replace('&quot;', '"')) for x in partes]
body = ''.join(partes)

# cada célula leva o nome da coluna, para as tabelas empilharem no celular
def rotula(m):
    tab = m.group(0)
    heads = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<th[^>]*>(.*?)</th>', tab, re.S)]
    def linha(mm):
        cels = re.findall(r'<td[^>]*>.*?</td>', mm.group(0), re.S)
        novo = mm.group(0)
        for i, c in enumerate(cels):
            if i == 0 or i >= len(heads):
                continue
            novo = novo.replace(c, c.replace('<td', '<td data-label="%s"' % heads[i].replace('"', ''), 1), 1)
        return novo
    return re.sub(r'<tr>\s*<td.*?</tr>', linha, tab, flags=re.S)
body = re.sub(r'<table.*?</table>', rotula, body, flags=re.S)

# caixa de principais pontos
n = body.count('<blockquote>')
assert n == 1, n
body = body.replace('<blockquote>', '<blockquote class="pontos">')

capa = ('<img class="capa" src="{{HERO_URL}}" width="1200" height="630" '
        'alt="Capa do guia de marketing para clínica odontológica, com a agenda de uma clínica cheia de pacientes vindos dos anúncios" '
        'fetchpriority="high" decoding="async">')
bloco = '<article id="dbout-artigo">\n' + capa + '\n' + body + '\n</article>'
wp = '<!-- wp:html -->\n' + bloco + '\n<!-- /wp:html -->\n'
assert '—' not in wp and '–' not in wp
open(out, 'w', encoding='utf-8').write(wp)
print('bytes', len(wp), 'h2', wp.count('<h2'), 'tabelas', wp.count('<table'), 'svg', wp.count('<svg'))
