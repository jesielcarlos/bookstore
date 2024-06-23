# Use uma imagem oficial do Python como imagem base
FROM python:3.10.12

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto para o diretório de trabalho
COPY . /app/

# Exponha a porta que o Django usará
EXPOSE 8000

# Execute as migrações, colete arquivos estáticos e inicie o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
