# 🛒 E-Commerce Web Application

A feature-rich e-commerce backend API built with Django and Django REST Framework.  
It includes secure authentication, international payment integration via Stripe, real-time order notifications via Telegram Bot, and asynchronous task management with Celery, Redis, and RabbitMQ.

---

## 🚀 Features

- ✅ JWT-based Authentication (Register, Login, Logout)
- 💳 Stripe Integration for secure international payments
- 📦 Order Management with product, cart, and checkout functionality
- 🤖 Telegram Bot Integration for real-time order alerts
- ⚙️ Asynchronous task queue using Celery + Redis + RabbitMQ
- 🧾 Swagger/OpenAPI documentation for API testing
- 🛠️ Admin panel for product, user, and order control

---

## 🛠️ Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Authentication:** JWT (Djoser)
- **Payments:** Stripe API
- **Async Tasks:** Celery, Redis, RabbitMQ
- **Notifications:** Telegram Bot API
- **Database:** PostgreSQL
- **API Docs:** Swagger (drf-yasg)

---

## 📷 Screenshots *(optional)*
<!-- Add screenshots or API doc images here -->

---

## 🧪 Installation & Run Locally

```bash
# Clone the repo
git clone https://github.com/OzodbekPrimov/e_commerse_2.git
cd e_commerse_2

# Create virtual environment & activate
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env file)
# Add your Stripe keys, Telegram bot token, etc.

# Run migrations
python manage.py migrate

# Run server
python manage.py runserver
