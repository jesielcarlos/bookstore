from dataclasses import dataclass
from datetime import timezone
from apps.core.exceptions import DefaultException
from apps.core.helpers import GoogleBooksAPI, Helpers, ResponseAPI
from apps.core.models import Book, ItemOrder, Order
from src.__seedwork.application.use_cases import UseCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm


@dataclass(slots=True)
# class ListBooksUseCase(UseCase, Helpers):

#     def execute(self, **kwargs):
#         try:
#             api = GoogleBooksAPI()
#             response = api.search_books(kwargs.get("query"))
#             if response['totalItems'] == 0:
#                 response = None
#             return response
#         except Exception as e:
#             raise DefaultException(detail=str(e), code=HTTP_400_BAD_REQUEST)


@dataclass
class ListBooksUseCase(UseCase, Helpers):

    def execute(self, categoria='', nome_livro='', nome_autor=''):
        api = GoogleBooksAPI()
        query = ''
        
        if nome_livro:
            query += f'intitle:{nome_livro} '
        if nome_autor:
            query += f'inauthor:{nome_autor} '
        if categoria:
            query += f'subject:{categoria} '

        response = api.search_books(query.strip())
        return response
    

@dataclass
class AddToCartUseCase:

    def execute(self, request, book_id):
        api = GoogleBooksAPI()
        book_data = api.get_book(book_id)
        authors = None
        categories = None
        if 'authors' in book_data['volumeInfo']:
                authors = ', '.join(book_data['volumeInfo']['authors'])
                if len(authors) > 200:
                    authors = authors[:200]

        if 'categories' in book_data['volumeInfo']:
            categories = ', '.join(book_data['volumeInfo']['categories'])
            if len(categories) > 200:
                categories = categories[:200]
        if 'publishedDate' not in book_data['volumeInfo']:
            book_data['volumeInfo']['publishedDate'] = ''
        book, created = Book.objects.get_or_create(
            google_books_id=book_data['id'],
            defaults={
                'title': book_data['volumeInfo']['title'],
                'authors': authors if authors is not None else '',
                'categories': categories if categories is not None else '',
                'publishedDate': book_data['volumeInfo']['publishedDate'],
                'price': book_data['saleInfo']['listPrice']['amount'],
                'thumbnail': book_data['volumeInfo']['imageLinks']['thumbnail']
            }
        )

        order_id = request.session.get('order_id')
        if order_id:
            order = Order.objects.get(id=order_id)
        else:
            order = Order.objects.create()
            request.session['order_id'] = order.id
        
        item_order = ItemOrder.objects.create(
            order=order,
            book=book,
        )


@dataclass
class CartUseCase:

    def execute(self, request):
        order_id = request.session.get('order_id')
        if order_id:
            order = ItemOrder.objects.filter(order__id=order_id)
            for i in order:
                print(i)
            return order
        else:
            order = None
            return order


@dataclass
class CheckoutGetUseCase:

    def execute(self, request):
        order_id = request.session.get('order_id')
        if order_id:
            order = ItemOrder.objects.filter(order__id=order_id)
            return order
        else:
            return None


@dataclass
class CheckoutPostUseCase:

    def execute(self, request):
        order_id = request.session.get('order_id')
        if order_id:
            order = Order.objects.get(id=order_id)
            order.is_open = False
            order.customer = request.user
            order.save()
            del request.session['order_id']
            return order
        else:
            return None


@dataclass
class RegisterPostUseCase:

    def execute(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return form, user
        return None


@dataclass
class OrderhistoryUseCase:

    def execute(self, request):
        orders = Order.objects.filter(customer=request.user, is_open=False)
        return orders
