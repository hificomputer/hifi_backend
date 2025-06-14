from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import FeedBack, Notification, Order

User = get_user_model()

@receiver(post_save, sender=FeedBack)
def create_feedback_notification(sender, instance, created, **kwargs):
    if created:
        staff_users = User.objects.filter(is_staff=True)
        for user in staff_users:
            Notification.objects.create(
                user=user,
                message=f"New feedback from {str(instance.user)}",
                n_type="feedback",
                related_id=instance.id
            )


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    total_items, total_amount = instance.cart.cart_total()
    shipping_charge = settings.SHIPPING_CHARGES.get(instance.location, 0) * total_items
    discount_amount =  0
    if instance.coupon:
        discount_amount = instance.coupon.get_discount_amount(total_amount)
        instance.coupon_discount_amount = discount_amount
    if instance.shipping_charge == 0:
        instance.shipping_charge = shipping_charge
    instance.payable = total_amount + shipping_charge - discount_amount


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        # set cartproduct sale_price to product selling price
        for cart_product in instance.cart.cartproduct_set.all():
            cart_product.sale_price = cart_product.product.selling_price
            cart_product.save()