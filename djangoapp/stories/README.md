# Construção do visualizador de Webstories

Este roteiro começa no estado atual do projeto. Não refaça banco, admin, view
ou URL antes de iniciar estas etapas.

## O que já está pronto

- `Story`, `StorySlide` e `StoryElement` já estão modelados e migrados.
- O admin já permite cadastrar stories, slides e elementos.
- Os elementos já possuem tipo, texto, cor do texto, cor de fundo, posição,
  animação, atraso, ordem e parceiro afiliado.
- `StoryDetailView` já carrega somente stories publicadas.
- Slides e elementos já chegam ordenados e com consultas otimizadas.
- A URL `stories:detail` já abre uma story pelo `slug`.
- `story_detail.html` já comprova que título, imagens e elementos chegam ao
  template.
- A `LandingPageView` já envia `stories` publicadas para a landing page.
- A seção visual e o carrossel de Webstories da landing page já existem, mas
  os cards ainda usam imagens, textos e links temporários.

O trabalho restante está dividido nas quatro etapas abaixo.

## Etapa 1 — Montar a estrutura completa do visualizador no HTML

### Objetivo

Transformar o template de teste `story_detail.html` na estrutura real do
visualizador. Nesta etapa, ainda não é necessário fazer animações nem troca
automática de slides.

### O que fazer

1. Criar um contêiner que ocupe a página e forme o fundo externo do
   visualizador.
2. Dentro dele, criar o palco vertical da story. Esse é o retângulo central
   onde a imagem e os textos serão exibidos.
3. Criar no topo do palco:
   - uma barra de progresso para cada slide;
   - o botão de pausar;
   - o botão de compartilhar.
4. Manter o loop `story.slides.all`, mas transformar cada slide em um painel
   próprio. Todos podem existir no HTML, porém somente um receberá a classe de
   slide ativo.
5. Dentro de cada painel, renderizar:
   - `slide.image` como imagem de fundo visual;
   - os elementos de `slide.elements.all` sobre a imagem.
6. Converter os valores do banco em classes ou atributos do HTML:
   - `position` separa os elementos em `top`, `center` ou `bottom`;
   - `element_type` diferencia `title`, `text`, `badge` e `cta`;
   - `animation` informa qual animação será executada;
   - `delay_ms` deve ir para um atributo `data-*` ou variável CSS;
   - `variant` fornece a cor do texto;
   - `background_color` fornece o fundo somente quando não estiver vazio.
7. Para um elemento `cta`, renderizar um link usando:
   - `element.affiliate_partner.affiliate_url` como destino;
   - `element.affiliate_partner.button_label` como texto;
   - abertura segura em outra aba.
8. Criar os botões anterior e próximo fora do palco, um em cada lateral.

### Resultado esperado

Ao abrir `/stories/slug-da-story/`, todos os dados corretos devem existir no
HTML. Apenas o primeiro slide deve aparecer, mesmo que a troca de slides ainda
não funcione.

## Etapa 2 — Construir o visual com CSS

### Objetivo

Reproduzir o formato vertical mostrado na referência: story centralizada,
laterais escuras, imagem ocupando todo o palco e textos posicionados sobre a
foto.

### O que fazer

1. Fazer o contêiner externo ocupar a área visível da janela e centralizar o
   palco horizontal e verticalmente.
2. Dar ao palco proporção `9 / 16`, altura limitada à tela e largura calculada
   a partir dessa altura. Assim ele permanece vertical sem usar dimensões
   rígidas para todos os dispositivos.
3. Usar `position: relative` no palco. Imagem, elementos, progresso e controles
   internos serão posicionados em relação a ele.
4. Fazer cada slide ocupar exatamente o palco e esconder os slides que não
   possuem a classe ativa.
5. Fazer a imagem preencher o painel com `width`, `height` e
   `object-fit: cover`.
6. Criar três regiões transparentes sobre a imagem:
   - superior para `position="top"`;
   - central para `position="center"`;
   - inferior para `position="bottom"`.
7. Estilizar separadamente título, texto, destaque e CTA. A cor dinâmica deve
   vir das propriedades fornecidas no HTML, não de uma cor fixa para todos os
   elementos.
8. Quando `background_color` estiver vazio, deixar o texto sem fundo. Quando
   houver uma cor, aplicar o fundo apenas ao bloco daquele elemento.
9. Colocar barras de progresso e botões internos acima dos demais conteúdos
   usando camadas coerentes de `z-index`.
10. Posicionar anterior e próximo nas laterais externas no desktop. Em telas
    estreitas, mantê-los acessíveis sem provocar rolagem horizontal.

### Resultado esperado

O primeiro slide deve ficar visualmente próximo da referência em desktop e
celular: imagem vertical central, texto nas regiões cadastradas, cores
corretas, barras no topo e controles visíveis. Ainda não precisa avançar.

## Etapa 3 — Programar o funcionamento com JavaScript

### Objetivo

Controlar qual slide está ativo, o tempo de exibição, os botões e as barras de
progresso.

### O que fazer

1. Criar um arquivo JavaScript exclusivo do visualizador e carregá-lo no fim
   de `story_detail.html`.
2. Selecionar a lista de slides, barras de progresso e botões de controle.
3. Manter um índice que represente o slide atual.
4. Criar uma única função responsável por exibir um índice. Ela deve:
   - remover o estado ativo do slide anterior;
   - ativar o slide solicitado;
   - atualizar as barras concluídas, atual e futuras;
   - reiniciar o temporizador;
   - reiniciar as animações dos elementos daquele slide.
5. Ligar essa função aos botões anterior e próximo.
6. Criar o avanço automático após o tempo definido para cada slide.
7. Fazer o botão de pausa interromper tanto o avanço quanto o progresso e,
   quando acionado novamente, continuar de onde parou.
8. Ler `animation` e `delay_ms` de cada elemento para que eles apareçam na
   ordem cadastrada no admin.
9. Impedir que um clique no CTA seja interpretado como comando para avançar o
   slide.
10. Ao chegar ao último slide, escolher um comportamento único: encerrar a
    reprodução ou voltar ao primeiro. Não misturar os dois comportamentos.

### Resultado esperado

Anterior, próximo, pausa, avanço automático, barras de progresso e animações
devem permanecer sincronizados mesmo depois de navegar para frente e para
trás várias vezes.

## Etapa 4 — Ligar a landing page e finalizar a experiência

### Objetivo

Substituir os cards temporários pelos dados reais e preparar o visualizador
para uso normal.

### O que fazer

1. Na landing page, trocar os oito cards escritos manualmente por um loop em
   `stories`.
2. Em cada card, usar:
   - `story.cover.url` na imagem;
   - `story.title` no título;
   - `{% url 'stories:detail' story.slug %}` no link.
3. Manter as classes exigidas pelo Swiper para não quebrar o carrossel já
   existente.
4. Implementar o compartilhamento com a Web Share API e fornecer uma
   alternativa de copiar o endereço quando o navegador não oferecer essa API.
5. Adicionar navegação por teclado, nomes acessíveis nos botões, foco visível
   e respeito a `prefers-reduced-motion`.
6. Confirmar que toda imagem possui `alt_text` útil e que links afiliados
   mantêm seus atributos de segurança e identificação comercial.
7. Testar pelo menos estes casos:
   - story com um único slide;
   - story com vários slides;
   - slide sem elementos;
   - vários elementos na mesma posição;
   - texto sem fundo e texto com fundo;
   - CTA afiliado;
   - story não publicada;
   - desktop e celular.
8. Criar testes Django para publicação, ordem dos dados, resposta da URL e
   conteúdo renderizado. O comportamento do JavaScript deve ser conferido no
   navegador.

### Resultado esperado

Um card real da landing page abre sua story, todos os slides funcionam no
visualizador e o conteúdo cadastrado no admin controla textos, posições,
cores, animações e CTA sem alterar manualmente o template para cada story.
