from django.db import models
from django.contrib.auth.models import User

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    data_publicacao = models.DateField()
    capa_url = models.URLField()
    sinopse = models.TextField(blank=True)
    numero_paginas = models.IntegerField(blank=True, null=True)
    publicadora = models.CharField(max_length=200, blank=True)
    google_books_id = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.titulo


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    livros = models.ManyToManyField(Livro, through='ItemPedido')

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.username}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade} x {self.livro.titulo}"
