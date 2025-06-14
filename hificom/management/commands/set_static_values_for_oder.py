from typing import Any
from django.core.management import BaseCommand
from hificom.models import Order


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        orders = Order.objects.all()
        carts = [o.cart for o in orders]
        for order in orders:
            total_items, cart_total = order.cart.cart_total()
            shipping_charge = order.shipping_charge
            if order.coupon:
                order.coupon_discount_amount = order.coupon.get_discount_amount(cart_total)
            if shipping_charge == 0:
                shipping_charge = order.location.shipping_charges * total_items
                order.shipping_charge = shipping_charge
                order.save()
        for cart in carts:
            for cart_product in cart.cartproduct_set.all():
                if cart_product.sale_price == 0 and cart_product.sale_price != cart_product.product.selling_price:
                    cart_product.sale_price = cart_product.product.selling_price
                    cart_product.save()