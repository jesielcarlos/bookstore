# Livraria Online

Este é um projeto Django para uma livraria online que permite aos usuários visualizar livros, adicionar livros ao carrinho e finalizar compras.

## Pré-requisitos

Antes de começar, certifique-se de ter o Docker e o Docker Compose instalados na sua máquina. Você pode instalar o Docker [aqui](https://docs.docker.com/get-docker/) e o Docker Compose [aqui](https://docs.docker.com/compose/install/).

## Configuração do Projeto

### 1. Clonar o Repositório

Clone este repositório para sua máquina local usando o seguinte comando:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```
### 2. Gerar um secret_key para o projeto, criando um arquivo .py com o seguinte código

```bash
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
### 2. Criar arquivo .env na raiz do projeto
```bash
SECRET_KEY=
POSTGRES_USER=user
POSTGRES_PASSWORD=123
POSTGRES_DB=bookstore
DATABASE_URL=postgres://user:123@db:5432/bookstore
DEFAULT_CACHE_URL=redis://redis_service:6379/0
GOOGLE_BOOKS_API_URL=https://www.googleapis.com/books/v1/volumes
API_KEY=AIzaSyBBdWfCKxl1GLqI9lIz_HXkmWZaz9tuhWA
```

## 3. Executar o comando
```bash
docker-compose up (Para ver logs)

docker-compose up -d (Sem logs)
```