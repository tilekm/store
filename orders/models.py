from django.db import models

from products.models import Basket, Product
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = [
        [CREATED, 'Создан'],
        [PAID, 'Оплачен'],
        [ON_WAY, 'В пути'],
        [DELIVERED, 'Доставлен'],
    ]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'

    def is_order_available(self):
        available = True
        baskets = Basket.objects.filter(user=self.initiator)
        for basket in baskets:
            product = Product.objects.get(id=basket.product_id)
            if basket.quantity > product.quantity:
                basket.delete()
                available = False
        return True if available else False

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        json_list = []
        for basket in baskets:
            product = Product.objects.get(id=basket.product_id)
            product.quantity -= basket.quantity
            product.save()
            json_list.append(basket.de_json())
        self.basket_history = {
            'purchased_items': json_list,
            'total_sum': float(baskets.total_sum())
        }
        self.save()
        baskets.delete()
