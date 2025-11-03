# Projeto de blog em Django

Este projeto, é um blog desenvolvido por Ygor Lima como parte da conclusão do curso de Python sob instrução do professor Luiz Otávio Miranda.

# Tecnlogias Utilizadas 
- Pythob 3.11
- Django
- Docker 
- Postgre
- HTML
- Servidor Gunicorn para servir Django
- Servidor NGINX para servir arquivos Státicos

# Comandos Docker:
- docker-compose run --build
- docker-compose run
- docker-compose down -v


# Relação de models neste projeto 

MenuLink tem um campo:
``` 

site_setup = models.ForeignKey('SiteSetup', on_delete=models.CASCADE)

```

Isso cria uma relação de muitos para um (many-to-one):

Muitos MenuLink podem estar ligados a um mesmo SiteSetup.