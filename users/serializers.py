from rest_framework import serializers

from users.models import User, Payments

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ("id", "user", "payment_date", "course", "lesson", "amount", 'payment_method')


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "city", "payments",)
