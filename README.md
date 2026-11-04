# Dbout Mídia, site novo

Rebranding da página inicial de dboutmidia.com, construído com a skill Hallmark
(tema Dose: papel quente, tinta verde-preta, um verde de farmácia como único sinal).
Prévia: https://manualdotrafego.github.io/dbout-site/

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html`, `styles.css`, `tokens.css`, `base.css` | a página, pronta para abrir no navegador |
| `assets/` | logo em tinta, Luis recortado, parede do escritório, stills dos depoimentos, logos de clientes, capturas do quiz, filme da jornada |
| `elementor-dbout-home.json` | template do Elementor, gerado por `exportar_elementor.py` |
| `exportar_elementor.py` | regenera o JSON (`python3 exportar_elementor.py [URL base dos assets]`) |
| `.hallmark/` | log do build, capturas do linter |

## Importar no WordPress

1. Elementor, Templates, Templates salvos, Importar templates: envie `elementor-dbout-home.json`.
2. Abra a página inicial no Elementor, insira o template e publique. O template já pede o
   layout "Elementor Canvas" (sem cabeçalho e rodapé do tema).
3. Os assets apontam para o GitHub Pages. Para hospedar no próprio WordPress: suba a pasta
   `assets/` na Biblioteca de mídia (ou por FTP em `wp-content/uploads/dbout/`) e gere o JSON de novo
   com a URL: `python3 exportar_elementor.py https://dboutmidia.com/wp-content/uploads/dbout`.

Cada seção é um widget HTML com nome próprio na árvore do Elementor, então dá para
reordenar ou esconder pelo editor. O CSS inteiro está no primeiro widget.

## No WordPress (dboutmidia.com)

Publicado em 2026-11-04. A página inicial é a página **3066** ("Página Principal 2026",
slug `inicio-2026`, template Elementor Canvas), criada no editor do Elementor a partir do
modelo importado **3097** (biblioteca, "Dbout Mídia, página inicial (rebranding)"). A antiga
página inicial (id **9**, "Página Principal") continua publicada; para voltar, em
Configurações > Leitura escolha a página 9 como inicial. As imagens e o filme são servidos
pelo GitHub Pages (`manualdotrafego.github.io/dbout-site/assets/`): se o repositório sair
do ar, a página perde as imagens; mover os assets para a mídia do WordPress é o próximo passo.
Para atualizar o conteúdo: editar `index.html`, rodar `python3 exportar_elementor.py`,
importar o JSON na biblioteca do Elementor e inserir na página (ou substituir os widgets HTML).

## v2 (variação para validar)

`v2.html` é a mesma página com outro hero: fotografia de madrugada em tela cheia, navegação
sobreposta e um painel de vidro com "a noite de ontem" (números ilustrativos). Gerado por
`python3 tools_build_v2.py` a partir do `index.html`, então rode de novo depois de qualquer
edição na página principal. Estilos em `v2.css`. A foto é "Secrets Beneath the Fog" de
SAFEOWN, Wikimedia Commons, CC BY-SA 4.0 (crédito no canto do hero); para o site final,
trocar por foto própria ou licenciada e remover o crédito.

## Imagem do hero

`assets/hero-agenda.html` é a ilustração do hero (a agenda de uma segunda-feira com sete
pacientes novos vindos dos anúncios e uma mensagem respondida em quatro minutos), desenhada no
material da página. Para alterar nomes, horários ou o número, edite o HTML e renderize:
`node tools_render_hero.mjs "$PWD/assets/hero-agenda.html" "$PWD/assets/hero-agenda.png"`
(usa o puppeteer-core da skill Hallmark e o Chrome instalado), depois gere os webp de 720 e
1200 px com PIL. Fotos do Luis foram tentadas e descartadas (recorte e retrato).

## Filme da jornada

`assets/jornada.mp4` e `.webm` saem do Remotion em `~/Downloads/dbout-motion`
(composição `Jornada`, dados em `public/jornada.json`): seis passos de 4,2 s, 27 s no total,
sem narração. A trilha é original, gerada na API de música do ElevenLabs
(`public/musica_jornada.mp3`, prompt no script musica.py do scratchpad da sessão; versão
cortada em 27 s com fade e loudnorm em `musica_jornada_27.mp3`). A narração com a voz do
Luis foi gravada e descartada; o áudio ficou em `public/narr_jornada.mp3` caso volte.
Na página o filme roda mudo em loop; dois ícones redondos controlam som (liga e recomeça do
zero) e pausa. Para re-renderizar:
`npx remotion render src/index.ts Jornada out/jornada.mp4` e copiar mp4, webm e poster para `assets/`.

## Lacunas marcadas na página

- Nomes e cidades dos quatro depoentes (`data-fill="depoentes"`).
- Endereço do escritório (`data-fill="endereco"`).
- Fora da página: CNPJ e WhatsApp comercial, se quiserem no rodapé.
