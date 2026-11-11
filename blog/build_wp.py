"""Monta o HTML do post para o WordPress na identidade do site (tema Dose).
uso: build_wp2.py <html renderizado> <saida.wp.html> [<saida de teste standalone>]
"""
import re, sys
src, out = sys.argv[1], sys.argv[2]
teste = sys.argv[3] if len(sys.argv) > 3 else None
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

# caixa de principais pontos
n = body.count('<blockquote>')
assert n == 1, n
body = body.replace('<blockquote>', '<blockquote class="pontos">')

css = '''/* Hallmark · shape: Long Read · genre: editorial · theme: Dose, identidade do site Dbout (by request) · job: read · draw: dbout-guia
 * hero: capa do guia · nav: sumário em duas colunas · footer: lista de fontes · posture: restrained · surface: paper */
html,body{overflow-x:clip}
:root{--db-paper:oklch(97.6% 0.011 88);--db-paper-2:oklch(96.5% 0.02 160);--db-paper-3:oklch(93% 0.036 160);--db-ink:oklch(21% 0.025 170);--db-muted:oklch(42% 0.024 165);--db-rule:oklch(86.5% 0.022 140);--db-accent:oklch(50% 0.13 160);--db-accent-deep:oklch(38% 0.1 162);--db-display:"Schibsted Grotesk",ui-sans-serif,sans-serif;--db-body:"Instrument Sans",ui-sans-serif,sans-serif}
.elementor-widget-container:has(> #dbout-artigo){background-color:var(--db-paper);box-shadow:none;border:1px solid var(--db-rule);border-radius:16px;padding:48px 24px}
#dbout-artigo{max-width:41rem;margin:0 auto;color:var(--db-ink);font-family:var(--db-body);font-size:1.125rem;line-height:1.65}
#dbout-artigo p,#dbout-artigo li,#dbout-artigo td,#dbout-artigo th,#dbout-artigo figcaption{color:var(--db-ink);font-family:var(--db-body);font-weight:400}
#dbout-artigo p{margin:0 0 1.25rem;text-wrap:pretty}
#dbout-artigo h2,#dbout-artigo h3{color:var(--db-ink);font-family:var(--db-display);font-weight:600;letter-spacing:-0.01em;text-wrap:balance}
#dbout-artigo h2{font-size:clamp(1.5rem,1.25rem + 1.2vw,2rem);line-height:1.15;margin:3.5rem 0 1rem;padding-top:2rem;border-top:1px solid var(--db-rule)}
#dbout-artigo h3{font-size:clamp(1.125rem,1.05rem + 0.4vw,1.3125rem);line-height:1.3;margin:2rem 0 0.75rem}
#dbout-artigo strong{color:inherit;font-weight:600}
#dbout-artigo ul,#dbout-artigo ol{margin:0 0 1.25rem;padding-left:1.5rem}
#dbout-artigo li{margin:0 0 0.5rem}
#dbout-artigo a{color:var(--db-accent-deep);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px;overflow-wrap:anywhere}
#dbout-artigo a:hover{color:var(--db-ink)}
#dbout-artigo a:focus-visible{outline:2px solid var(--db-accent);outline-offset:2px;border-radius:2px}
#dbout-artigo a:active{color:var(--db-accent)}
#dbout-artigo .capa{display:block;width:100%;height:auto;margin:0 0 2rem;border:1px solid var(--db-rule);border-radius:12px}
#dbout-artigo .pontos{margin:2rem 0;padding:1.5rem;background:var(--db-paper-3);border:1px solid var(--db-rule);border-radius:12px}
#dbout-artigo .pontos p{margin:0 0 0.75rem;font-family:var(--db-display);font-weight:600}
#dbout-artigo .pontos ul{margin:0}
#dbout-artigo .pontos li:last-child{margin:0}
#dbout-artigo .sumario{margin:2rem 0 0;padding:1.5rem 0;border-top:1px solid var(--db-rule);border-bottom:1px solid var(--db-rule)}
#dbout-artigo .sumario__t{margin:0 0 0.75rem;font-family:var(--db-display);font-weight:600;font-size:1rem;color:var(--db-muted)}
#dbout-artigo .sumario ul{margin:0;padding:0;list-style:none;columns:2;column-gap:2rem;font-size:1rem;line-height:1.4}
#dbout-artigo .sumario li{margin:0 0 0.5rem;break-inside:avoid}
#dbout-artigo .sumario a{color:var(--db-ink);text-decoration-color:var(--db-rule)}
#dbout-artigo .sumario + h2{margin-top:2.5rem;padding-top:0;border-top:0}
#dbout-artigo .table-wrap{margin:2rem 0;overflow-x:auto}
#dbout-artigo table{width:100%;margin:0;border-collapse:collapse;font-size:0.9375rem;line-height:1.5;font-variant-numeric:tabular-nums}
#dbout-artigo th,#dbout-artigo td{padding:0.75rem;border:0;border-bottom:1px solid var(--db-rule);background-color:transparent;text-align:left;vertical-align:top}
#dbout-artigo th{font-weight:600;background-color:var(--db-paper-3)}
#dbout-artigo figure.blog-chart{margin:2.5rem 0;padding:1.5rem 0.5rem 1rem;background:var(--db-paper-2);border:1px solid var(--db-rule);border-radius:12px}
#dbout-artigo figure.blog-chart svg{display:block;width:100%;max-width:40rem;height:auto;margin:0 auto;color:var(--db-ink);font-family:var(--db-body);--chart-muted:var(--db-muted)}
#dbout-artigo figure.blog-chart rect,#dbout-artigo figure.blog-chart circle{fill:var(--db-accent)}
#dbout-artigo figure.blog-chart line{stroke:var(--db-accent)}
#dbout-artigo figcaption{margin:0.75rem 0 0;font-size:0.875rem;color:var(--db-muted);text-align:center}
@media (max-width:40rem){.elementor-widget-container:has(> #dbout-artigo){padding:24px 16px;border-radius:12px}#dbout-artigo{font-size:1.0625rem}#dbout-artigo h2{margin-top:3rem}#dbout-artigo .sumario ul{columns:1}#dbout-artigo table{min-width:34rem}}
'''

fontes = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600&amp;family=Schibsted+Grotesk:wght@600&amp;display=swap">')
capa = ('<img class="capa" src="{{HERO_URL}}" width="1200" height="630" '
        'alt="Capa do guia de marketing para clínica odontológica, com a agenda de uma clínica cheia de pacientes vindos dos anúncios" '
        'fetchpriority="high" decoding="async">')
bloco = fontes + '\n<style>' + css + '</style>\n<article id="dbout-artigo">\n' + capa + '\n' + body + '\n</article>'
wp = '<!-- wp:html -->\n' + bloco + '\n<!-- /wp:html -->\n'
assert '—' not in wp and '–' not in wp
open(out, 'w', encoding='utf-8').write(wp)
print('bytes', len(wp), 'h2', wp.count('<h2'), 'tabelas', wp.count('<table'), 'svg', wp.count('<svg'))

if teste:
    # página de teste: simula o cartão do modelo do blog em volta do artigo
    pagina = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
              '<title>Guia de marketing odontológico</title></head><body><main><div class="elementor-widget-container">'
              + bloco.replace('{{HERO_URL}}', 'hero.png') + '</div></main></body></html>')
    open(teste, 'w', encoding='utf-8').write(pagina)
