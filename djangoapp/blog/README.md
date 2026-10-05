# Tool MCP para atualizar posts

## Objetivo

A tool `PostTools.update_post`, localizada em `blog/mcp.py`, deve conseguir
atualizar os campos de um post e também alterar somente um trecho específico de
`Post.content`.

`Post.content` continua sendo o mesmo `TextField`. Não é necessário alterar o
modelo, criar outro modelo ou migrar os posts existentes.

## Leitura do post

Antes de atualizar o conteúdo, a LLM deve chamar `show_post_detail`. A resposta
deve retornar o HTML exatamente como está salvo:

```json
{
  "id": 10,
  "title": "Título do post",
  "content": "<h2>Planos</h2><table><tr><td>R$ 29,90</td></tr></table>",
  "content_revision": "ed07d8592f..."
}
```

`content_revision` é um hash SHA-256 calculado a partir do conteúdo atual. Ele
permite verificar se o post mudou entre a leitura e a atualização.

```python
import hashlib


def calculate_content_revision(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
```

## Atualização parcial

A mesma `update_post` recebe os campos comuns em `changes` e as alterações do
conteúdo em `content_patches`:

```json
{
  "post_id": 10,
  "changes": {
    "title": "Novo título"
  },
  "expected_content_revision": "ed07d8592f...",
  "content_patches": [
    {
      "target_html": "<td>R$ 29,90</td>",
      "replacement_html": "<td>R$ 39,90</td>"
    }
  ]
}
```

- `target_html` é o trecho exato existente no conteúdo atual.
- `replacement_html` é o trecho que entrará no lugar.
- O alvo pode ser qualquer HTML: parágrafo, título, lista, tabela, linha,
  célula, imagem ou seção.
- Se o alvo aparecer mais de uma vez, a atualização deve ser recusada. A LLM
  deverá enviar um trecho maior e único.
- Se o hash estiver desatualizado, a atualização deve ser recusada e o post
  deverá ser lido novamente.

## Fluxo da tool

`update_post` deve:

1. carregar o post atual com `select_for_update()`;
2. validar os campos recebidos em `changes`;
3. comparar `expected_content_revision` com o hash do conteúdo atual;
4. aplicar cada substituição sobre o `Post.content` atual;
5. validar o post com `full_clean()`;
6. salvar somente os campos modificados usando `update_fields`.

A LLM envia somente o trecho que deseja modificar. Ela não deve gerar nem enviar
novamente todo o conteúdo do post.

Como `content` é uma única coluna `TextField`, o banco recebe o valor final dessa
coluna ao salvar. Entretanto, a tool preserva o conteúdo atual e modifica apenas
os trechos indicados pelos patches.
