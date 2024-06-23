from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(
        verbose_name='Titulo',
        max_length=200
    )
    authors = models.CharField(
        verbose_name='Autor',
        max_length=200
    )
    categories = models.CharField(
        verbose_name='Categoria',
        max_length=100
    )
    publishedDate = models.CharField(
        verbose_name='Data de Publicação',
        max_length=100
    )
    thumbnail = models.CharField(
        verbose_name='Capa',
        max_length=200
    )
    pageCount = models.IntegerField(
        verbose_name='Número de páginas',
        blank=True,
        null=True
    )
    publisher = models.CharField(
        verbose_name='Editora',
        max_length=200,
        blank=True
    )
    google_books_id = models.CharField(
        verbose_name='ID no Google Books',
        max_length=200,
        unique=True
    )
    selfLink = models.CharField(
        verbose_name='Link de detalhes',
        max_length=200
    )
    description = models.TextField(
        verbose_name='Descrição',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        verbose_name='Preço',
        max_digits=10,
        decimal_places=2
    )


    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name='Cliente',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    order_date = models.DateTimeField(
        verbose_name='Data do pedido', 
        auto_now_add=True
    )
    books = models.ManyToManyField(
        Book,
        verbose_name='Livros',
        through='ItemOrder'
    )

    def __str__(self):
        return f"Pedido {self.id} de {self.customer.username}"


class ItemOrder(models.Model):
    pedido = models.ForeignKey(
        Order,
        verbose_name='Pedido',
        on_delete=models.DO_NOTHING)
    livro = models.ForeignKey(
        Book,
        verbose_name='Livro',
        on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(
        verbose_name='Quantidade',
        default=1
    )

    def __str__(self):
        return f"{self.quantidade} - {self.livro.titulo}"
