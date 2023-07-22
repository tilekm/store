from celery import shared_task

from orders.models import Order


@shared_task
def fulfill_order(order_id):
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
