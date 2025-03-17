
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Order
from .task import send_order_notification


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:  # Faqat yangi order yaratilganda ishlaydi
        # Celery task-ni chaqirish

        phone_number = instance.phone_number if instance.phone_number else "Telefon raqam kiritilmagan"
        send_order_notification.delay(
            order_id=instance.id,
            customer=str(instance.customer),
            phone_number=phone_number,
            product=str(instance.product),
            quantity=instance.quantity,
            created_at=str(instance.created_at)
        )



