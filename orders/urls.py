from django.urls import path

from orders.views import (CancelTemplateView, OrderCreateView, OrderDetailView,
                          OrdersListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='detail'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('success/', SuccessTemplateView.as_view(), name='success'),
    path('cancel/', CancelTemplateView.as_view(), name='cancel'),
]
