"""Gera as peças do modelo de post do blog (Elementor single 1053) e uma página de teste.

uso: python3 build_modelo.py
saídas:
  widget-topo.html   widget HTML do topo: link de pular, fontes, <style> com blog.css e o cabeçalho
  widget-pe.html     widget HTML do rodapé
  modelo-post.html   página de teste que imita a marcação do Elementor em volta dos widgets dinâmicos
"""
import re
from pathlib import Path

AQUI = Path(__file__).parent
SITE = 'https://dboutmidia.com'
ASSETS = 'https://manualdotrafego.github.io/dbout-site/assets'
DIAG = 'https://manualdotrafego.github.io/diagnostico-dbout/'

css = (AQUI / 'blog.css').read_text(encoding='utf-8')
assert css.startswith('/* Hallmark')

fontes = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500&amp;family=Schibsted+Grotesk:wght@700&amp;display=swap">')

topo = f'''<a class="blog-skip" href="#blog-corpo">Ir para o conteúdo</a>
<nav class="blog-bar" aria-label="Principal">
  <div class="blog-container">
    <a class="wordmark" href="{SITE}/" aria-label="Dbout Mídia, início"><img src="{ASSETS}/wordmark-ink.png" width="731" height="132" alt=""></a>
    <div class="blog-bar__links">
      <a href="{SITE}/#frentes">O trabalho</a>
      <a href="{SITE}/#jornada">A jornada</a>
      <a href="{SITE}/#clientes">Clientes</a>
      <a class="blog-bar__blog" href="{SITE}/blog/">Blog</a>
      <a class="btn" href="{DIAG}">Fazer o diagnóstico</a>
    </div>
  </div>
</nav>'''

pe = f'''<footer class="blog-foot">
  <div class="blog-container">
    <div class="blog-foot__sign">
      <p>Se a agenda da sua clínica depende de indicação, a gente conversa. Se já investe em tráfego e não vê paciente novo, também.</p>
      <b>Luis Parrela, fundador da Dbout Mídia</b>
    </div>
    <ul class="blog-foot__links">
      <li><a href="{SITE}/">Página inicial</a></li>
      <li><a href="{SITE}/blog/">Blog da Dbout</a></li>
      <li><a href="{SITE}/marketing-para-clinica-odontologica/">Guia de marketing para clínica odontológica</a></li>
      <li><a href="https://www.instagram.com/dboutmidia">Instagram da Dbout</a></li>
      <li><a href="https://www.youtube.com/@Dbout_Midia">Canal no YouTube</a></li>
      <li><a href="{DIAG}">Diagnóstico gratuito</a></li>
    </ul>
    <div class="blog-foot__legal">
      <img src="{ASSETS}/wordmark-ink.png" width="731" height="132" alt="Dbout Mídia">
      <span>Dbout Mídia Ltda, CNPJ 50.704.575/0001-63. Av. Brigadeiro Faria Lima, 2369, conj. 1102, Jardim Paulistano, São Paulo, SP, CEP 01452-922.</span>
    </div>
  </div>
</footer>'''

widget_topo = fontes + '\n<style>\n' + css + '</style>\n' + topo + '\n'
widget_pe = pe + '\n'
for nome, txt in (('widget-topo.html', widget_topo), ('widget-pe.html', widget_pe)):
    assert '—' not in txt and '–' not in txt
    (AQUI / nome).write_text(txt, encoding='utf-8')

# ---- página de teste: a marcação do Elementor em volta dos widgets dinâmicos ----
conteudo = (AQUI / 'marketing-para-clinica-odontologica.wp.html').read_text(encoding='utf-8')
conteudo = re.sub(r'<!-- /?wp:html -->\n?', '', conteudo).replace('{{HERO_URL}}', 'marketing-para-clinica-odontologica.png')


def w(tipo, miolo, extra=''):
    return (f'<div class="elementor-element elementor-widget elementor-widget-{tipo}{extra}">'
            f'<div class="elementor-widget-container">{miolo}</div></div>')


def con(ident, miolo, tag='div'):
    return f'<{tag} class="elementor-element e-flex e-con-boxed e-con e-parent" id="{ident}"><div class="e-con-inner">{miolo}</div></{tag}>'


relacionados = ''.join(
    f'''<article class="elementor-post elementor-grid-item post type-post">
<a class="elementor-post__thumbnail__link" href="{SITE}/{slug}/" tabindex="-1"><div class="elementor-post__thumbnail"><img width="{iw}" height="{ih}" src="{img}" alt=""></div></a>
<div class="elementor-post__text"><h3 class="elementor-post__title"><a href="{SITE}/{slug}/">{titulo}</a></h3>
<div class="elementor-post__meta-data"><span class="elementor-post-date">{data}</span></div>
<div class="elementor-post__read-more-wrapper"><a class="elementor-post__read-more" href="{SITE}/{slug}/" aria-label="Ler o artigo {titulo}" tabindex="-1">Ler o artigo</a></div></div></article>'''
    for slug, titulo, data, img, iw, ih in (
        ('como-usar-dois-whatsapp-business-em-um-unico-dispositivo-android', 'Como Usar Dois WhatsApp Business em um Único Dispositivo Android', '10 de setembro de 2024', f'{SITE}/wp-content/uploads/2023/11/1.webp', 480, 270),
        ('a-importancia-do-trafego-pago-para-captar-novos-clientes-na-area-da-saude', 'A Importância do Tráfego Pago para Captar Novos Clientes na Área da Saúde', '13 de agosto de 2024', f'{SITE}/wp-content/uploads/2024/08/Sem-nome-1280-x-1280-px.png', 1280, 1280),
        ('a-importancia-do-crm-e-follow-up-no-recebimento-de-leads-na-area-da-saude', 'A Importância do CRM e Follow-up no Recebimento de Leads na Área da Saúde', '14 de agosto de 2024', f'{SITE}/wp-content/uploads/2024/08/Sem-nome-1280-x-1280-px.png', 1280, 1280),
    ))

comentarios = '''<section id="comments" class="comments-area"><div id="respond" class="comment-respond">
<h2 id="reply-title" class="comment-reply-title">Deixe um comentário</h2>
<form action="#" method="post" id="commentform" class="comment-form" novalidate>
<p class="comment-notes"><span id="email-notes">O seu endereço de e-mail não será publicado.</span> <span class="required-field-message">Campos obrigatórios são marcados com <span class="required">*</span></span></p>
<p class="comment-form-comment"><label for="comment">Comentário <span class="required">*</span></label> <textarea id="comment" name="comment" cols="45" rows="8" maxlength="65525" required></textarea></p>
<p class="comment-form-author"><label for="author">Nome <span class="required">*</span></label> <input id="author" name="author" type="text" value="" size="30" maxlength="245" autocomplete="name" required></p>
<p class="comment-form-email"><label for="email">E-mail <span class="required">*</span></label> <input id="email" name="email" type="email" value="" size="30" maxlength="100" aria-describedby="email-notes" autocomplete="email" required></p>
<p class="comment-form-url"><label for="url">Site</label> <input id="url" name="url" type="url" value="" size="30" maxlength="200" autocomplete="url"></p>
<p class="comment-form-cookies-consent"><input id="wp-comment-cookies-consent" name="wp-comment-cookies-consent" type="checkbox" value="yes"> <label for="wp-comment-cookies-consent">Salvar meus dados neste navegador para a próxima vez que eu comentar.</label></p>
<p class="form-submit"><input name="submit" type="submit" id="submit" class="submit" value="Publicar comentário"></p>
</form></div></section>'''

pagina = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Marketing para clínica odontológica: como captar pacientes</title>
<meta name="description" content="Como captar pacientes para clínica odontológica com anúncios, WhatsApp e Perfil no Google, com dados do Brasil, métricas e as regras do CFO.">
</head>
<body class="single single-post elementor-page-1053">
<div class="elementor elementor-1053 elementor-location-single">
{con('blog-topo', w('html', widget_topo))}
{con('blog-corpo', '<header class="elementor-element e-con e-child" id="blog-capa">' + w('theme-post-title', '<h1 class="elementor-heading-title elementor-size-default">Marketing para clínica odontológica: como captar pacientes</h1>', ' elementor-page-title elementor-widget-heading') + w('post-info', '<ul class="elementor-inline-items elementor-icon-list-items elementor-post-info"><li class="elementor-icon-list-item elementor-inline-item"><span class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"><span class="elementor-post-info__item-prefix">Publicado em </span><time>11 de novembro de 2026</time></span></li></ul>') + '</header>' + w('ha-post-content', conteudo), 'main')}
{con('blog-comentarios', w('ha-post-comments', comentarios), 'section')}
{con('blog-mais', w('heading', '<h2 class="elementor-heading-title elementor-size-default">Veja outros artigos</h2>') + w('posts', '<div class="elementor-posts-container elementor-posts elementor-posts--skin-classic elementor-grid">' + relacionados + '</div>', ' elementor-grid-3'), 'section')}
{con('blog-pe', w('html', widget_pe), 'footer')}
</div>
</body>
</html>
'''
(AQUI / 'modelo-post.html').write_text(pagina, encoding='utf-8')
print('widget-topo', len(widget_topo), '| widget-pe', len(widget_pe), '| modelo-post', len(pagina))
