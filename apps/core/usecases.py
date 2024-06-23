from dataclasses import dataclass
from apps.core.exceptions import DefaultException
from apps.core.helpers import GoogleBooksAPI, Helpers, ResponseAPI
from apps.core.models import Book, ItemOrder, Order
from src.__seedwork.application.use_cases import UseCase
from rest_framework.status import (
    HTTP_200_OK,
)


@dataclass(slots=True)
class ListBooksUseCase(UseCase, Helpers):

    def execute(self, **kwargs):
        api = GoogleBooksAPI()
        response = api.search_books(kwargs.get("query"))
        return response


@dataclass
class AddToCartUseCase:

    def execute(self, request, book_id):
        api = GoogleBooksAPI()
        book_data = api.get_book(book_id)
        
        # Verifica se o livro já existe na tabela Book, caso contrário, cria um novo
        book, created = Book.objects.get_or_create(
            id=book_data['id'],
            defaults={
                'title': book_data['volumeInfo']['title'],
                'author': ', '.join(book_data['volumeInfo']['authors']),
                'category': ', '.join(book_data['volumeInfo']['categories']),
                'published_date': book_data['volumeInfo']['publishedDate'],
                'price': book_data['saleInfo']['listPrice']['amount'],
                'thumbnail': book_data['volumeInfo']['imageLinks']['thumbnail']
            }
        )

        # Verifica se o usuário tem um pedido aberto
        order = Order.objects.get_or_create(
            books=book
        )
        
        # Verifica se o item do pedido já existe, caso contrário, cria um novo
        item_order, created = ItemOrder.objects.get_or_create(
            pedido=order,
            livro=book,
            defaults={'quantity': 1}
        )

        if not created:
            # Se o item já existe, incrementa a quantidade
            item_order.quantity += 1
            item_order.save()
