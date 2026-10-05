from pydantic import BaseModel, ConfigDict, Field, field_validator

class PostCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: str = Field(
        min_length=1,
        max_length=125,
        description=(
            "Título do post. "
            "Não envie uma string vazia."
        ),
    )
    
    excerpt: str = Field(
        min_length=1,
        max_length=160,
        description=(
            "Resumo do post. Não envie uma string vazia."
        )
    )
    
    content: str = Field(
        min_length=1,
        description=(
            "Conteúdo completo do post em HTML. "
            "Pode conter parágrafos, títulos, listas, tabelas, imagens e links."
        ),
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("content não pode ficar vazio.")

        return value
    
    slug: str | None = Field(
        default=None,
        max_length=255,
        description=(
            "Slug do post. Omita, envie null ou uma string vazia "
            "para gerar automaticamente a partir do título."
        ),
    )

    category_id: int | None = Field(
        default=None,
        ge=1,
        description=(
            "ID da categoria do post. "
            "Omita ou envie null para criar o post sem categoria."
        ),
    )

    tag_ids: list[int] | None = Field(
        default=None,
        description=(
            "IDs das tags do post. "
            "Omita, envie null ou uma lista vazia para criar o post sem tags."
        ),
    )

class ContentPatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    target_html: str = Field(
        min_length=1,
        description="Trecho HTML exato existente no conteúdo.",
    )
    
    replacement_html: str = Field(
        description="HTML que substituirá o trecho encontrado.",
    )

class PostChangesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=125,
        description=(
            "Novo título do post. Omita para manter o título atual. "
            "Não envie uma string vazia."
        ),
    )
    
    slug: str | None = Field(
        default=None,
        max_length=255,
        description=(
            "Novo slug do post. Omita para manter o slug atual. "
            "Envie null ou uma string vazia para gerar o slug novamente."
        )
    )
    
    excerpt: str | None = Field(
        default=None,
        min_length=1,
        max_length=160,
        description=(
            "Novo resumo do post. Omita para manter o resumo atual. "
            "Não envie uma string vazia."
        ),
    )
    
    category_id: int | None = Field(
        default=None,
        ge=1,
        description=(
            "ID da nova categoria. Omita para manter a categoria atual. "
            "Envie null para remover a categoria."
        ),
    )
    
    tag_ids: list[int] | None = Field(
        default=None,
        description=(
            "Lista completa de IDs das tags. Omita para manter as tags "
            "atuais. Envie uma lista vazia para remover todas as tags."
        ),
    )
    
    
    
