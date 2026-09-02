# Deploy para a VPS

Este roteiro publica o **Rota Asiática** sem expor o Django diretamente na
internet. O Nginx da VPS termina o HTTPS e encaminha apenas para
`127.0.0.1:8001`, onde o contêiner Gunicorn responde.

> Execute os comandos da VPS como um usuário com `sudo`. Substitua todos os
> valores entre `<...>` antes de executar.

## 1. Preparar DNS e acesso

No provedor do domínio, crie um registro `A` apontando o domínio para o IP
público da VPS. Exemplo:

```text
rotaasiatica.com      A      <IP_DA_VPS>
www.rotaasiatica.com  A      <IP_DA_VPS>
```

Na sua máquina, confirme a propagação antes de pedir o certificado HTTPS:

```bash
dig +short rotaasiatica.com
dig +short www.rotaasiatica.com
```

Crie um usuário exclusivo para deploy na VPS e permita Docker e sudo:

```bash
sudo adduser deploy
sudo usermod -aG sudo,docker deploy
```

Saia e entre novamente com esse usuário para o grupo `docker` ser reconhecido.
Depois, adicione sua chave SSH pública em
`/home/deploy/.ssh/authorized_keys` e confirme o acesso:

```bash
ssh deploy@<IP_DA_VPS>
```

## 2. Instalar dependências da VPS

Se Docker, Git e Certbot ainda não existirem na VPS Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose-plugin nginx certbot python3-certbot-nginx
sudo systemctl enable --now docker nginx
```

Confira as versões:

```bash
docker compose version
git --version
nginx -v
certbot --version
```

## 3. Baixar o projeto no servidor

Entre como `deploy` e clone a branch de produção em um diretório fixo:

```bash
sudo mkdir -p /opt/rota-asiatica
sudo chown deploy:deploy /opt/rota-asiatica
git clone git@github.com:ygorlima-py/projeto-blog-django.git /opt/rota-asiatica
cd /opt/rota-asiatica
git switch main
```

Se o repositório for privado, crie uma chave SSH de leitura para a VPS e
cadastre a chave pública como **Deploy key** no GitHub antes do `git clone`:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/rota_asiatica_repository -C "vps-rota-asiatica"
cat ~/.ssh/rota_asiatica_repository.pub
```

No GitHub, abra `Settings > Deploy keys > Add deploy key`, cole a chave pública
e deixe **Allow write access** desmarcado.

## 4. Criar o ambiente de produção

Copie o modelo seguro, mantenha esse arquivo fora do Git e abra-o para edição:

```bash
cd /opt/rota-asiatica
cp dotenv_files/.env.production-example dotenv_files/.env
chmod 600 dotenv_files/.env
nano dotenv_files/.env
```

Gere uma `SECRET_KEY` nova na VPS:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

No arquivo `.env`, preencha pelo menos estes valores reais:

```dotenv
SECRET_KEY="<CHAVE_GERADA_ACIMA>"
DEBUG="0"
DJANGO_ENV="production"
ALLOWED_HOSTS="rotaasiatica.com,www.rotaasiatica.com"
CSRF_TRUSTED_ORIGINS="https://rotaasiatica.com,https://www.rotaasiatica.com"
TRUST_X_FORWARDED_PROTO="1"
SECURE_SSL_REDIRECT="1"
SESSION_COOKIE_SECURE="1"
CSRF_COOKIE_SECURE="1"
SECURE_HSTS_SECONDS="31536000"
POSTGRES_DB="rota_asiatica"
POSTGRES_USER="rota_asiatica"
POSTGRES_PASSWORD="<SENHA_LONGA_E_ALEATORIA>"
POSTGRES_HOST="psql"
POSTGRES_PORT="5432"
```

Use uma senha diferente para o banco e não cole nenhum desses valores no GitHub
ou em mensagens públicas.

## 5. Preparar diretórios persistentes

O banco, os uploads e os arquivos estáticos sobrevivem à recriação dos
contêineres em `data/`. Crie os diretórios:

```bash
cd /opt/rota-asiatica
mkdir -p data/web/static data/web/media data/postgres/data
```

O Django roda como um usuário não-root dentro do contêiner. Descubra seu UID e
ajuste a propriedade dos diretórios web antes do primeiro `collectstatic`:

```bash
APP_UID=$(docker compose run --rm --no-deps djangoapp id -u)
APP_GID=$(docker compose run --rm --no-deps djangoapp id -g)
sudo chown -R "$APP_UID:$APP_GID" data/web
sudo chmod -R u+rwX,go+rX data/web
```

Se o Postgres apontar erro de permissão no primeiro boot, descubra o usuário da
imagem e corrija somente o diretório do banco:

```bash
POSTGRES_UID=$(docker run --rm postgres:17-alpine id -u postgres)
POSTGRES_GID=$(docker run --rm postgres:17-alpine id -g postgres)
sudo chown -R "$POSTGRES_UID:$POSTGRES_GID" data/postgres/data
sudo chmod 700 data/postgres/data
```

## 6. Primeiro início e validação Django

Construa e inicie os serviços:

```bash
cd /opt/rota-asiatica
docker compose up --build -d
docker compose ps
docker compose logs --tail=100 djangoapp
```

O serviço `djangoapp` deve aparecer como `Up`. Em produção ele executa
migrations existentes, coleta estáticos e inicia Gunicorn. Ele **não** cria
migrations automaticamente.

Rode o checklist de produção:

```bash
docker compose exec -T djangoapp python manage.py check --deploy
```

## 7. Configurar Nginx e HTTPS

Crie primeiro o arquivo HTTP abaixo em
`/etc/nginx/sites-available/rota-asiatica`. Troque os domínios:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name rotaasiatica.com www.rotaasiatica.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
```

Habilite o site sem alterar a configuração da aplicação já existente:

```bash
sudo mkdir -p /var/www/certbot
sudo ln -s /etc/nginx/sites-available/rota-asiatica /etc/nginx/sites-enabled/rota-asiatica
sudo nginx -t
sudo systemctl reload nginx
```

Gere o certificado:

```bash
sudo certbot --nginx -d rotaasiatica.com -d www.rotaasiatica.com
```

Depois do Certbot, complete o bloco HTTPS criado por ele com estas localizações
(mantenha as diretivas `ssl_*` que o Certbot criou):

```nginx
client_max_body_size 12m;

location /static/ {
    alias /opt/rota-asiatica/data/web/static/;
    access_log off;
    expires 30d;
}

location /media/ {
    alias /opt/rota-asiatica/data/web/media/;
    expires 7d;
}

location / {
    proxy_pass http://127.0.0.1:8001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_redirect off;
}
```

Valide e recarregue após editar:

```bash
sudo nginx -t
sudo systemctl reload nginx
curl -I https://rotaasiatica.com
```

Não abra a porta `8001` no firewall: ela está limitada a `127.0.0.1` e somente
o Nginx local deve acessá-la.

## 8. Habilitar CI obrigatório no GitHub

O arquivo `.github/workflows/ci.yml` roda em todo pull request para `main` e
depois de cada merge. Ele executa `check`, verifica migrations, roda todos os
testes e executa `check --deploy`.

Para impedir merge sem aprovação dos testes, no GitHub abra:

```text
Settings > Branches > Add branch protection rule
```

Configure a regra para `main` e marque:

1. **Require a pull request before merging**;
2. **Require status checks to pass before merging**;
3. selecione o check `CI / Django` após a primeira execução;
4. **Require branches to be up to date before merging**;
5. **Do not allow bypassing the above settings**;
6. desative force pushes e exclusões da branch.

O workflow não faz merge por conta própria. A proteção da branch é que bloqueia
o botão de merge até o check ficar verde.

## 9. Habilitar deploy automático pelo GitHub Actions

O workflow `.github/workflows/deploy-vps.yml` só executa após uma CI bem-sucedida
na `main` e permanece inativo até `DEPLOY_ENABLED=true` ser criado. Antes de
habilitar, configure o ambiente `production` em:

```text
Settings > Environments > New environment > production
```

Se quiser aprovar cada deploy, adicione seu usuário em **Required reviewers**.
Depois crie estes **Actions secrets** no repositório:

| Secret | Valor |
| --- | --- |
| `VPS_HOST` | IP ou hostname da VPS |
| `VPS_PORT` | normalmente `22` |
| `VPS_USER` | `deploy` |
| `VPS_SSH_KEY` | chave privada exclusiva do GitHub Actions |
| `VPS_KNOWN_HOSTS` | saída verificada de `ssh-keyscan -H <IP_DA_VPS>` |

Crie uma chave exclusiva para o GitHub Actions, adicione a parte pública em
`/home/deploy/.ssh/authorized_keys` da VPS e cadastre a parte privada em
`VPS_SSH_KEY`:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/rota_asiatica_github_actions -C "github-actions-rota-asiatica"
ssh-keyscan -H <IP_DA_VPS>
```

Adicione também estes **Actions variables**:

| Variável | Valor |
| --- | --- |
| `VPS_DEPLOY_PATH` | `/opt/rota-asiatica` |
| `DEPLOY_ENABLED` | `true` somente depois do primeiro deploy manual funcionar |

Após um PR passar pela CI e for mesclado na `main`, o workflow conecta por SSH,
faz checkout exatamente do commit aprovado pela CI, reconstrói os contêineres e
aguarda o Gunicorn aceitar conexões. O `check --deploy` é executado pelo próprio
contêiner antes de iniciar o Gunicorn, sem criar outro processo Django em paralelo.
Se o deploy falhar, o workflow ficará vermelho e o site
anterior normalmente continua em execução.

## 10. Deploy manual, atualização e rollback

Para uma atualização manual segura na VPS:

```bash
cd /opt/rota-asiatica
git pull --ff-only origin main
docker compose up --build -d
docker compose exec -T djangoapp python manage.py check --deploy
docker compose logs --tail=100 djangoapp
```

Para voltar ao commit anterior, primeiro descubra os commits e escolha o hash
anterior validado:

```bash
cd /opt/rota-asiatica
git log --oneline -10
git checkout <HASH_ANTERIOR>
docker compose up --build -d
docker compose exec -T djangoapp python manage.py check --deploy
```

Depois do rollback, não faça `git pull` até investigar a falha. Para retornar à
branch principal quando estiver pronto:

```bash
git switch main
git pull --ff-only origin main
```

## 11. Backup

Faça backup do banco com `pg_dump` e dos uploads em `data/web/media/`. Exemplo:

```bash
cd /opt/rota-asiatica
mkdir -p backups
docker compose exec -T psql sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > "backups/blog-$(date +%F).sql"
tar -czf "backups/media-$(date +%F).tar.gz" data/web/media
```

Copie os backups para fora da VPS (outro provedor, bucket ou disco local). Teste
uma restauração em ambiente separado antes de depender dela em uma emergência.
