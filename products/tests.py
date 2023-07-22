from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory

# Create your tests here.


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('home')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(
            list(response.context_data['categories']),
            list(ProductCategory.objects.all())
        )

    def test_products_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(Product.objects.filter(id__lte=3))
        )

    def text_categories_list(self):
        category = ProductCategory.objects.get(id=1)
        path = reverse('products:category', args=(category.id))
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(Product.objects.filter(category_id=category.id))
        )
