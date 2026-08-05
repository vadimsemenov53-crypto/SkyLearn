import stripe
from config.settings import STRIPE_API_KEY
from materials.models import Course

stripe.api_key = STRIPE_API_KEY

def create_stripe_product(object_course: Course):
    """ Функция создания продукта в Stripe. """
    product = stripe.Product.create(
        name=object_course.name,
        description = object_course.description
    )

    return product


def create_stripe_price(product, amount):
    """ Создает цену в Страйпе. """

    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product.id,
    )


def create_stripe_session(price_id):
    """ Создает сессию на оплату. """
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/success",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )

    return session.id, session.url
