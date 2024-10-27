
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'portfolio', 'theme', 'newsletter_freq', 'phone_number', 'risk_pref']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, data):
            user = data['username']
            pass1 = data['password']
            email = data['email']
            phone = data['phone_number']
            user_email_validated = 0

            user = CustomUser(username=user, email=email, phone_number=phone)
            user.set_password(pass1)
            user.save()
            return user