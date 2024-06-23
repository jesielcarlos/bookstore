from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from apps.core.models import ItemOrder, Order
from apps.core.usecases import AddToCartUseCase, CartUseCase, CheckoutGetUseCase, CheckoutPostUseCase, ListBooksUseCase, OrderhistoryUseCase, RegisterPostUseCase
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm


class HomeView(View):
    template_name = "home.html"

    #@method_decorator(cache_page(60 * 1))
    def get(self, request):
        categoria = request.GET.get('category', '')
        nome_livro = request.GET.get('book', '')
        nome_autor = request.GET.get('author', '')

        response = ListBooksUseCase().execute(
            categoria=categoria,
            nome_livro=nome_livro,
            nome_autor=nome_autor
        )
        
        return render(request, self.template_name, {'ctx': response})


class AddToCartView(View):
    def post(self, request, book_id):
        response = AddToCartUseCase().execute(request, book_id=book_id)
        return redirect(reverse('home'))


class CartView(View):
    def get(self, request):
        order = CartUseCase().execute(request)
        return render(request, 'cart.html', {'order': order})


class CheckoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        order = CheckoutGetUseCase().execute(request)
        return render(request, 'checkout.html', {'order': order})

    @method_decorator(login_required)
    def post(self, request):
        order = CheckoutPostUseCase().execute(request)
        return redirect('order_history')


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form, user = RegisterPostUseCase().execute(request)
        if form.is_valid():
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})


class OrderHistoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        orders = OrderhistoryUseCase().execute(request)
        return render(request, 'order_history.html', {'orders': orders})
