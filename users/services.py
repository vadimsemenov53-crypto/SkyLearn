import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

def create_stripe_product(course):
    """ Функция создания продукта в Stripe. """
    product = stripe.Product.create(
        name=course.name,
        description = course.description
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


def create_stripe_payment(course):
    """ Вспомогательная функция объединяющая логику для Stipe (create_product / price / session) """
    product = create_stripe_product(course)
    price = create_stripe_price(product, course.amount)

    return create_stripe_session(price.id)
