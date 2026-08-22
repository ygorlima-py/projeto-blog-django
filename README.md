# Rota Asiática

Blog em Django para publicar relatos sobre a vida na Tailândia, viagens e o
Sudeste Asiático.

## Tecnologias atuais

- Python 3.11
- Django 5.2
- PostgreSQL 17
- Docker e Docker Compose
- Django Summernote para edição de conteúdo
- Django Axes para proteção da área administrativa
- HTML e CSS renderizados pelo Django

O ambiente local usa `manage.py runserver`. Para produção, o contêiner inicia
Gunicorn quando `DJANGO_ENV="production"`; o Nginx continua sendo configurado
no servidor, como proxy reverso e terminador de HTTPS.

## Como executar

Crie o arquivo de ambiente na primeira execução:

```bash
cp dotenv_files/.env-example dotenv_files/.env
```

No Docker, `POSTGRES_HOST` deve ser `psql` e `POSTGRES_PORT` deve ser `5432`.
Depois, execute:

```bash
docker compose up --build
```

Neste ambiente, o blog está publicado em <http://localhost:8001/> e o painel
administrativo em <http://localhost:8001/admin/>.

Para criar um administrador:

```bash
docker compose exec djangoapp python manage.py createsuperuser
```

Quando você alterar modelos, gere a migration conscientemente e versione o
arquivo criado antes de subir o projeto. O contêiner não cria migrations sozinho:

```bash
docker compose exec djangoapp python manage.py makemigrations
docker compose exec djangoapp python manage.py migrate
```

Para encerrar os contêineres:

```bash
docker compose down
```

## Conteúdo pelo painel administrativo

1. `SITE_SETUP > Setup`: título, descrição, favicon e links do menu.
2. `BLOG > Categories`: categorias principais do conteúdo.
3. `BLOG > Tags`: assuntos específicos associados aos posts.
4. `BLOG > Posts`: artigos, resumos, capas, categorias e tags.
5. `BLOG > Pages`: páginas fixas, como "Sobre mim".

Uma página com slug `sobre-mim` usa o caminho `/page/sobre-mim/`. Uma
categoria com slug `viagens` usa `/category/viagens/`.

## Roteiro da evolução editorial

Este checklist registra as fontes de dados criadas para sustentar a interface
editorial e deve ser consultado nas próximas evoluções do projeto.

### 1. Perfil e avatar do autor

- [x] Criar `AuthorProfile` ligado ao `User` por `OneToOneField`.
- [x] Adicionar imagem de avatar opcional.
- [x] Permitir editar o perfil junto do usuário no Django Admin.
- [x] Criar automaticamente perfis para usuários novos e existentes.
- [x] Exibir avatar somente quando existir e manter fallback seguro.

### 2. Tempo estimado de leitura

- [x] Adicionar a propriedade `Post.reading_time`.
- [x] Calcular com base em 200 palavras por minuto.
- [x] Remover tags HTML do conteúdo antes da contagem.
- [x] Garantir o mínimo de um minuto.
- [x] Exibir `{{ post.reading_time }} min de leitura` nos metadados do post.

Essa propriedade é calculada em tempo de execução e não cria coluna no
banco de dados.

### 3. Post em destaque

- [x] Adicionar `Post.is_featured` com valor padrão `False`.
- [x] Disponibilizar o campo na listagem e nos filtros do Admin.
- [x] Ordenar posts em destaque antes dos demais, preservando a ordem recente.
- [x] Não exigir que todos os posts tenham capa, categoria ou autor.

### 4. Categorias para navegação

- [x] Criar um context processor do app `blog`.
- [x] Disponibilizar categorias que tenham posts publicados.
- [x] Evitar links para categorias vazias, pois essas páginas retornam 404.
- [x] Preservar os links manuais existentes em `site_setup.menu`.

### 5. Links sociais

- [x] Criar `SocialLink` relacionado ao `SiteSetup`.
- [x] Oferecer plataformas conhecidas e uma opção genérica.
- [x] Validar os endereços com `URLField`.
- [x] Editar links sociais como itens embutidos no `Setup` do Admin.
- [x] Exibir somente links cadastrados, sem inventar perfis ou URLs.

### 6. Integração e segurança dos templates

- [x] Preservar todos os nomes de URLs e variáveis de contexto atuais.
- [x] Proteger campos opcionais com `{% if %}`.
- [x] Aplicar o redesign visual preservando conteúdo e URLs existentes.
- [x] Higienizar o HTML do Summernote antes de armazenar e novamente ao renderizar.

### 7. Banco, testes e verificação

- [x] Gerar migrações versionadas para os novos campos e modelos.
- [x] Aplicar as migrações no PostgreSQL local.
- [x] Criar testes de modelos: tempo de leitura, destaque, categorias e perfil.
- [x] Criar testes das páginas públicas: posts, páginas, autor, categoria, tag,
  busca, paginação e URLs inexistentes.
- [x] Criar testes de acesso ao Admin e de visibilidade de rascunhos.
- [x] Criar testes de upload e redimensionamento de capas e avatares.
- [x] Criar testes para identidade e links de menu vindos do `SiteSetup`.
- [x] Executar `python manage.py check`.
- [x] Executar `python manage.py makemigrations --check --dry-run`.
- [x] Executar `python manage.py test`.

## Como usar os recursos editoriais

- **Avatar:** em `AUTENTICAÇÃO E AUTORIZAÇÃO > Usuários`, abra o autor e
  envie a imagem em `Perfil do autor > Avatar`.
- **Tempo de leitura:** é calculado automaticamente a partir do campo `Content`.
- **Destaque:** em `BLOG > Posts`, marque `Is featured`. Posts marcados aparecem
  antes dos demais.
- **Categorias:** a navegação mostra automaticamente categorias que possuem ao
  menos um post publicado.
- **Redes sociais:** em `SITE_SETUP > Setup`, edite a seção `Links sociais`,
  escolhendo plataforma, URL, rótulo opcional, ordem e abertura em nova aba.

## Interface editorial

A interface usa uma identidade editorial de viagem responsiva:

- verde-petróleo `#123d3a` como cor principal;
- terracota `#d96c43` como destaque;
- fundo marfim `#f7f3ea`;
- fonte Fraunces nos títulos e Manrope nos textos e controles;
- hero dinâmico, categorias em pills e grid de posts em 3/2/1 colunas;
- primeiro post em layout de destaque, respeitando a ordenação de
  `is_featured`;
- páginas de artigo e conteúdo com largura otimizada para leitura;
- navegação por teclado, foco visível e suporte a `prefers-reduced-motion`.

O nome, a descrição, o favicon, o menu e os links sociais não estão fixados nos
templates. Eles são lidos do cadastro `SITE_SETUP > Setup`, permitindo trocar a
identidade do blog pelo Admin sem editar o código.

## Mapa principal do projeto

```text
djangoapp/
├── blog/
│   ├── models.py       # Posts, páginas, categorias e tags
│   ├── views.py        # Listagens, busca e detalhes
│   ├── admin.py        # Configuração do Django Admin
│   ├── urls.py         # Rotas do blog
│   ├── templates/      # HTML renderizado pelo Django
│   └── static/         # CSS e JavaScript
├── site_setup/
│   ├── models.py       # Configuração global e menu
│   └── admin.py        # Edição do Setup
└── project/
    ├── settings.py     # Apps, banco, templates e arquivos
    └── urls.py         # Rotas principais
```

## Comandos de verificação

```bash
docker compose exec djangoapp python manage.py check
docker compose exec djangoapp python manage.py makemigrations --check --dry-run
docker compose exec djangoapp python manage.py test
```

## Segurança e produção

Os ajustes mais importantes já aplicados no código são:

- uploads do Summernote exigem autenticação e permissão de equipe (`is_staff`),
  com limite de 10 MB;
- o HTML de posts e páginas é sanitizado para bloquear scripts, eventos HTML e
  URLs perigosas antes de ser exibido;
- links do menu aceitam apenas caminhos internos, âncoras ou URLs HTTPS;
- em produção, o projeto falha ao iniciar sem `SECRET_KEY` segura ou
  `ALLOWED_HOSTS` definido;
- HTTPS, cookies seguros, HSTS, `nosniff` e política de referenciador são
  habilitados automaticamente fora do modo de desenvolvimento;
- Gunicorn é usado em produção e migrations não são geradas durante a inicialização.

Para publicar na VPS, copie `dotenv_files/.env.production-example` para
`dotenv_files/.env` e substitua todos os valores de exemplo. Use o domínio real
em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`. Não reutilize a chave local e não
envie o arquivo `.env` para o GitHub.

O Nginx do servidor deve encaminhar ao contêiner em `127.0.0.1:8001` e enviar
os cabeçalhos `Host`, `X-Forwarded-For` e `X-Forwarded-Proto`. Mantenha
`TRUST_X_FORWARDED_PROTO="1"` apenas quando esse cabeçalho for definido pelo
seu próprio Nginx. Antes de liberar o domínio, execute:

```bash
docker compose exec djangoapp python manage.py check --deploy
```

O banco e os uploads ficam em `data/`; faça backup regular de
`data/postgres/data/` e `data/web/media/`. Um dump com `pg_dump` é mais seguro
para restauração do PostgreSQL do que copiar somente os arquivos enquanto o banco
está em execução.

### O que a suíte de testes protege

- posts e páginas publicados versus rascunhos;
- detalhe, categoria, tag, autor, busca e paginação;
- retornos 404 para URLs inexistentes;
- tempo de leitura, post em destaque e categorias de navegação;
- acesso à área administrativa;
- upload, redimensionamento e exibição de capa e avatar;
- título, descrição e links de menu configurados pelo Admin.
- sanitização de conteúdo rico, permissões de upload e URLs seguras no menu.

Os testes ficam em `blog/tests.py`, `blog/test_views.py`,
`blog/test_admin.py`, `blog/test_media.py`, `blog/test_security.py` e
`site_setup/tests.py`.
O GitHub Actions deve executar os três comandos de verificação acima a cada
push e bloquear o deploy se algum deles falhar.

Arquivos em `dotenv_files/.env`, `data/postgres/` e `data/web/media/` não devem
ser versionados. Eles contêm configurações locais, banco e uploads.
