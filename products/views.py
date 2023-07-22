from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory

# Create your views here.


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsView(TitleMixin, ListView):
    model = Product
    paginate_by = 3
    title = 'Store - Каталог'
    template_name = 'products/products.html'
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product.id)

    if baskets.exists():
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        baskets.create(user=request.user, product=product, quantity=1)
    url = f'{request.META["HTTP_REFERER"]}#product_{product_id}'
    return HttpResponseRedirect(url)


@login_required
def basket_remove(request, basket_id):
    Basket.objects.filter(id=basket_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
