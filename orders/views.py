from http import HTTPStatus

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from orders.tasks import fulfill_order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrdersListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    model = Order
    ordering = '-created'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ №{self.object.id}'
        return context


class SuccessTemplateView(TitleMixin, TemplateView):
    title = 'Store - Спасибо за заказ!'
    template_name = 'orders/success.html'


class CancelTemplateView(TitleMixin, TemplateView):
    title = 'Store - Заказ отменён!'
    template_name = 'orders/cancel.html'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    title = 'Store - Оформление заказа'
    success_url = reverse_lazy('orders:create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        order = Order.objects.get(id=self.object.id)
        if not order.is_order_available():
            messages.error(request, 'Товар или товары из вашей корзины закончился! Пожалуйста попробуйте ещё раз!')
            return HttpResponseRedirect(reverse('orders:create'))
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:cancel')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Save an order in your database, marked as 'awaiting payment'
        create_order(session, request)

        # Check if the order is already paid (for example, from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            # Fulfill the purchase
            order_id = int(session.metadata.order_id)
            fulfill_order.delay(order_id)

    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        order_id = int(session.metadata.order_id)
        # Fulfill the purchase
        fulfill_order.delay(order_id)

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']

        # Email the customer asking them to retry their order
        email_customer_about_failed_payment(session)

    # Passed signature verification
    return HttpResponse(status=200)


def create_order(session, request):
    # TODO: fill me in
    pass


def email_customer_about_failed_payment(session):
    # TODO: fill me in
    pass
