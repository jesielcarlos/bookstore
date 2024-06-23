from django.urls import path
from apps.core.views import (
    AddToCartView,
    CartView,
    HomeView,
    OrderHistoryView
)

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('add_to_cart/<str:book_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('order_history/', OrderHistoryView.as_view(), name='order_history'),
]