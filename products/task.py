import time


import requests
from celery import shared_task

from config.settings import MY_CHAT_ID, BOT_TOKEN



@shared_task
def send_order_notification(order_id, customer, product, quantity, created_at, phone_number):
    time.sleep(5)  # 5 soniya kutish

    message = (
        f"Yangi buyurtma: {order_id}\n"
        f"Mijoz: {customer}\n"
        f"Tel raqam:{phone_number}\n"
        f"Mahsulot: {product}\n"
        f"quantity: {quantity}\n"
        f"Vaqt: {created_at}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Xabar yuborishda xato: {e}")
