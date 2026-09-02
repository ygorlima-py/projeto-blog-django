FROM python:3.11.14-alpine3.21
COPY --from=ghcr.io/astral-sh/uv:0.10.1 /uv /uvx /bin/

LABEL matainer="ygor.limarsx@gmail.com"

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Mantém o ambiente virtual fora do código montado como volume pelo
# Docker Compose durante o desenvolvimento.
ENV UV_PROJECT_ENVIRONMENT=/venv
ENV UV_LINK_MODE=copy
ENV PATH="/scripts:/venv/bin:$PATH"

# Copia primeiro apenas os arquivos de dependências para aproveitar o cache
# do Docker quando o código da aplicação mudar.
COPY pyproject.toml uv.lock /app/
COPY scripts /scripts

# Entra na raiz do projeto uv no container.
WORKDIR /app

# A porta 8000 estará disponível para conexões externas ao container
# É a porta que vamos usar para o Django.
EXPOSE 8000

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execução do comando é armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da 
# imagem e torná-la mais eficiente.
RUN uv sync --locked --no-dev --no-install-project --no-cache && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts

# O usuário da aplicação não possui diretório home; evita que comandos
# `uv run` tentem criar um cache em /home/duser.
ENV UV_NO_CACHE=1

# Copia o código Django depois da instalação das dependências.
COPY djangoapp /app/djangoapp

# Os scripts da aplicação executam o manage.py a partir desta pasta.
WORKDIR /app/djangoapp

# Muda o usuário para duser
USER duser

# Executa o arquivo scripts/commands.sh
CMD ["commands.sh"]
