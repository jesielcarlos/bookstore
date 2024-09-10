from django.urls import path
from apps.core.views import (
    AddToCartView,
    CartView,
    HomeView,
    OrderHistoryView
)
from django.contrib.auth import views as auth_views
from .views import RegisterView, CheckoutView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('add_to_cart/<str:book_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('order_history/', OrderHistoryView.as_view(), name='order_history'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('checkout/', CheckoutView.as_view(), name='checkout')
]
