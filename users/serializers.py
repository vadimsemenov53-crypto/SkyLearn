from rest_framework import serializers

from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "city",)


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ("id", "user", "payment_date", "course", "lesson", "amount", 'payment_method')
