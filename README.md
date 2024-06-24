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
### 2. Criar arquivo .env na raiz do projeto
```bash
SECRET_KEY=a5r69d@a8s45viyx1h1yqcuah2f771q614&8dcri
POSTGRES_USER=user
POSTGRES_PASSWORD=123
POSTGRES_DB=bookstore
DATABASE_URL=postgres://user:123@0.0.0.0:5432/bookstore
GOOGLE_BOOKS_API_URL=https://www.googleapis.com/books/v1/volumes
API_KEY=AIzaSyBBdWfCKxl1GLqI9lIz_HXkmWZaz9tuhWA
```

## 3. Executar o comando
```bash
docker-compose up (Para ver logs)

docker-compose up -d (Sem logs)
```