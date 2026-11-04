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

## Filme da jornada

`assets/jornada.mp4` e `.webm` saem do Remotion em `~/Downloads/dbout-motion`
(composição `Jornada`, dados em `public/jornada.json`). Hoje é mudo, com os seis passos
em tipografia. A narração com a voz do Luis entra depois da aprovação do roteiro em
`public/jornada_fala.txt`: gerar o áudio com timestamps, salvar `narr_jornada.mp3` e
`words`, apontar `narr` no JSON e renderizar de novo.

## Lacunas marcadas na página

- Nomes e cidades dos quatro depoentes (`data-fill="depoentes"`).
- Endereço do escritório (`data-fill="endereco"`).
- Fora da página: CNPJ e WhatsApp comercial, se quiserem no rodapé.
