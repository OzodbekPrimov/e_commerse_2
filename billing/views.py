
from django.conf import settings
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from billing.models import Payment
from products.models import Order
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY



class CreateChargeView(views.APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'stripe_token': openapi.Schema(type=openapi.TYPE_STRING, description='Stripe to‘lov tokeni'),
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Buyurtma ID’si'),
            },
            required=['stripe_token', 'order_id'],
        ),
        responses={
            200: openapi.Response('To‘lov muvaffaqiyatli', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'status': openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            400: 'Xato xabari'
        }
    )
    def post(self, request, *args, **kwargs):
        stripe_token = request.data.get('stripe_token') #userning karta ma'lumotlari
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error":"Order not fount"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            total_amount = order.product.price * order.quantity
            charge = stripe.Charge.create(
                amount=int(total_amount*100),
                currency='usd',
                source=stripe_token,
            )

            Payment.objects.create(
                order=order,
                stripe_charge_id=charge['id'],
                amount=total_amount
            )

            order.is_paid = True
            order.save()

            return Response({'status': "Payment successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
