from django.shortcuts import redirect, render
from django.views import View
from apps.core.models import Order
from apps.core.usecases import AddToCartUseCase, ListBooksUseCase
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.urls import reverse


class HomeView(View):
    template_name = "home.html"

    @method_decorator(cache_page(60 * 1))
    def get(self, request):
        #query = request.GET.get('query', '')
        query = "quimica+inauthor:Rozenberg"
        response = ListBooksUseCase().execute(query=query)
        
        return render(request, self.template_name, {'ctx': response})


class AddToCartView(View):
    def post(self, request, book_id):
        response = AddToCartUseCase().execute(request, book_id=book_id)
        return redirect(reverse('home'))


class CartView(View):
    def get(self, request):
        # Lógica para obter o carrinho do usuário
        order = Order.objects.filter(customer=request.user).first()
        return render(request, 'cart.html', {'order': order})

class OrderHistoryView(View):
    def get(self, request):
        # Lógica para obter o histórico de pedidos do usuário
        orders = Order.objects.filter(customer=request.user)
        return render(request, 'order_history.html', {'orders': orders})
