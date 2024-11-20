
from rest_framework import serializers
from .models import CustomUser
from pymongo import MongoClient
from django.conf import settings
from django.contrib.auth.hashers import make_password
import json
from bson.objectid import ObjectId

'''
{
    "username": "test_user4",
    "email": "royalgemcarbon@gmail.com",
    "password": "random"
}
'''

class CustomUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    portfolio = serializers.JSONField(required=False, default=list)
    theme = serializers.IntegerField(required=False, default=1)
    newsletter_freq = serializers.IntegerField(required=False, default=1)
    phone_number = serializers.CharField(required=False, allow_blank=True, default="")
    risk_pref = serializers.IntegerField(required=False, default=0)
    user_email_validated = serializers.BooleanField(required=False, default=False)
    user_validation_code = serializers.IntegerField(required=False, default=100000001)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])

        client = MongoClient('localhost', 27017)
        try:
            database = client['wsbdb']
            users = database['WSBapp_customuser']

            user_data = {
                '_id': ObjectId(),
                'username': validated_data.get('username'),
                'email': validated_data.get('email'),
                'password': validated_data.get('password'),
                'user_email_validated': validated_data.get('user_email_validated', False),
                'user_validation_code': validated_data.get('user_validation_code', 100000001),
                'portfolio': json.dumps(validated_data.get('portfolio', [])),
                'theme': validated_data.get('theme', 1),
                'newsletter_freq': validated_data.get('newsletter_freq', 1),
                'phone_number': validated_data.get('phone_number', ''),
                'risk_pref': validated_data.get('risk_pref', 0),
                'is_superuser': False,
                'is_staff': False,
                'is_active': True,
                'last_login': None,
                'date_joined': None
            }

            users.insert_one(user_data)
        finally:
            client.close()

        return user_data

'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'portfolio', 'theme',
            'newsletter_freq', 'phone_number', 'risk_pref',
            'user_email_validated', 'user_validation_code'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')

        user = CustomUser(username=username, email=email, user_email_validated=0)
        user.set_password(password)
        user.save()
        return user
    '''