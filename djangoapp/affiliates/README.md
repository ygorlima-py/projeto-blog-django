# Área de Parceiros — Manual de implementação

## Objetivo

Criar uma página comercial de parceiros afiliados com:

- filtros por categoria;
- cards com imagem, nome, descrição e botão;
- cadastro completo pelo Django Admin;
- ordenação de categorias e cards;
- somente itens publicados na área pública;
- links externos identificados como patrocinados.

## URLs públicas

```text
/parceiros/
/parceiros/categoria/<slug>/
```

Nomes das URLs:

```python
affiliates:list
affiliates:category
```

## Models

### AffiliateCategory

| Campo | Tipo | Regra |
|---|---|---|
| `name` | `CharField(60)` | Nome exibido no filtro |
| `slug` | `SlugField(unique=True)` | Gerado pelo Admin |
| `order` | `PositiveSmallIntegerField` | Menor número aparece primeiro |
| `is_active` | `BooleanField` | Categoria disponível publicamente |

Ordenação padrão:

```python
ordering = ('order', 'name')
```

### AffiliatePartner

| Campo | Tipo | Regra |
|---|---|---|
| `category` | `ForeignKey` | Usar `PROTECT` e `related_name='partners'` |
| `name` | `CharField(100)` | Nome da empresa ou serviço |
| `description` | `TextField(400)` | Texto simples, sem HTML |
| `image` | `ImageField` | `upload_to='affiliates/%Y/%m/'` |
| `image_alt` | `CharField(150)` | Texto alternativo da imagem |
| `affiliate_url` | `URLField(1000)` | Aceitar somente HTTPS |
| `button_label` | `CharField(40)` | Padrão: `Conhecer parceiro` |
| `order` | `PositiveSmallIntegerField` | Ordem dentro da categoria |
| `is_published` | `BooleanField` | Controla exibição pública |
| `created_at` | `DateTimeField` | `auto_now_add=True` |
| `updated_at` | `DateTimeField` | `auto_now=True` |

Ordenação padrão:

```python
ordering = ('order', 'name')
```

## Ordem de implementação

### 1. Registrar o app

Adicionar em `project/settings.py`:

```python
'affiliates',
```

### 2. Criar os models

Arquivo:

```text
affiliates/models.py
```

Regras obrigatórias:

- categoria não pode ser apagada enquanto possuir parceiros (`PROTECT`);
- descrição deve permanecer como texto simples;
- link deve começar com `https://`;
- categorias inativas não aparecem nos filtros;
- parceiros não publicados não aparecem na página.

### 3. Configurar o Admin

Arquivo:

```text
affiliates/admin.py
```

`AffiliateCategoryAdmin`:

- `list_display`: nome, ordem e ativa;
- `list_editable`: ordem e ativa;
- `prepopulated_fields`: slug a partir do nome;
- ordenação por `order` e `name`.

`AffiliatePartnerAdmin`:

- `list_display`: nome, categoria, ordem e publicado;
- `list_filter`: categoria e publicado;
- `search_fields`: nome e descrição;
- `list_editable`: ordem e publicado;
- `autocomplete_fields`: categoria;

### 4. Criar as URLs

Criar:

```text
affiliates/urls.py
```

Rotas:

```python
path('', AffiliateListView.as_view(), name='list')
path(
    'categoria/<slug:category_slug>/',
    AffiliateListView.as_view(),
    name='category',
)
```

Incluir em `project/urls.py`:

```python
path('parceiros/', include('affiliates.urls')),
```

### 5. Criar a view

Arquivo:

```text
affiliates/views.py
```

Usar `ListView` com:

- apenas `is_published=True`;
- apenas categorias ativas;
- `select_related('category')`;
- filtro opcional por `category_slug`;
- categoria inexistente ou inativa retorna `404`;
- `paginate_by = 12`;
- categorias com parceiros publicados no contexto;
- categoria ativa no contexto.

### 6. Criar o template

Criar:

```text
affiliates/templates/affiliates/partner_list.html
```

Estrutura:

1. título `Parceiros`;
2. traço laranja;
3. aviso de afiliados;
4. filtros em pills;
5. grid de cards;
6. paginação;
7. estado vazio quando não houver parceiros.

Aviso:

```text
Esta página reúne empresas e serviços divulgados por meio de programas
de afiliados. O Ásia de Perto pode receber uma comissão quando você realiza
uma compra ou reserva por estes links, sem custo adicional para você.
```

Link do card:

```html
target="_blank"
rel="sponsored noopener noreferrer"
```

### 7. Criar o CSS

Adicionar uma seção identificada como `/* Affiliates */` em:

```text
blog/static/blog/css/style.css
```

Layout:

- 3 colunas no desktop;
- 2 colunas no tablet;
- 1 coluna no celular;
- imagem com área consistente e `object-fit: contain`;
- categoria como pill clicável;
- descrição com altura visual limitada;
- botão no final do card;
- hover discreto;
- respeitar `prefers-reduced-motion` já existente.

### 8. Adicionar ao sitemap

Incluir:

- `/parceiros/`;
- categorias ativas que tenham parceiros publicados.

### 9. Adicionar ao menu

No `Site Setup`, criar um Menu Link:

```text
Texto: Parceiros
URL: /parceiros/
Exibir em: Cabeçalho e rodapé
```

## Testes obrigatórios

Criar testes para:

- página geral retorna `200`;
- parceiro publicado aparece;
- parceiro não publicado não aparece;
- categoria ativa filtra corretamente;
- categoria inativa retorna `404`;
- categoria inexistente retorna `404`;
- categorias respeitam a ordem;
- parceiros respeitam a ordem;
- link possui `rel="sponsored noopener noreferrer"`;
- link HTTP é rejeitado;
- descrição é escapada no HTML;
- página e categorias aparecem no sitemap.

## Comandos

Gerar e aplicar migração:

```bash
docker compose exec -T djangoapp python manage.py makemigrations affiliates
docker compose exec -T djangoapp python manage.py migrate
```

Verificar configuração:

```bash
docker compose exec -T djangoapp python manage.py check
docker compose exec -T djangoapp python manage.py makemigrations --check --dry-run
```

Executar testes:

```bash
docker compose exec -T djangoapp python manage.py test affiliates
docker compose exec -T djangoapp python manage.py test blog site_setup affiliates
```

## Critérios de conclusão

- [ ] Tudo pode ser cadastrado pelo Admin.
- [ ] Nenhum parceiro exige alteração de código para ser adicionado.
- [ ] Filtros funcionam por URL sem JavaScript.
- [ ] Cards são responsivos.
- [ ] Links comerciais são identificados com `sponsored`.
- [ ] Itens não publicados nunca aparecem publicamente.
- [ ] Sitemap inclui somente conteúdo ativo e publicado.
- [ ] Todos os testes passam.
