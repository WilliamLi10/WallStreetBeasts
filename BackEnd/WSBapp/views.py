from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.core.mail import send_mail
import random
from django.conf import settings
from .StockRecommendationManager import PortfolioAnalyzer
from .models import CustomUser
from django.conf import settings

# Create your views here.
@api_view(['GET'])
def landing_page(request):
    return Response({'test':'test'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username)
    print(password)

    is_valid = None
    if "@" in username:
        is_valid = authenticate(email=username, password=password)
    else:
        is_valid = authenticate(username=username, password=password)

    if is_valid is None:
        return Response({'error':'Wrong'}, status=400)
    else:
        token, created = Token.objects.get_or_create(user=is_valid)
        return Response({'token':token.key}, status=200)

@api_view(['POST'])    
def registration_view(request):
    print(settings.EMAIL_HOST_USER)
    print(settings.EMAIL_HOST_PASSWORD)
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    else:
        user = serializer.save()
        code = random.randint(100000001, 999999998)
        user.user_validation_code = code
        user.save()

        send_mail(
            subject='WallStreetBeasts Email Verification',
            message=("Hello "+user.username+", your code is "+str(code)+" please enter this code into the website to be able to validate your account!"),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        return Response(serializer.data, status=200)
    
@api_view(['POST'])
def logout_view(request):
    user = CustomUser.objects.filter(auth_token=request.auth).first()
    if user.is_authenticated:
        user.auth_token.delete()
        return Response({'message': 'Logged Out'}, status=200)
    else:
        return Response({'error': 'User not logged in'}, status=401)

@api_view(['POST'])
def verify_email_view(request):
    user = CustomUser.objects.filter(auth_token=request.auth).first()
    input_code = int(request.data.get('user_validation_code'))
    actual_code = user.user_validation_code

    if user is not None:
        if input_code == actual_code:
            user.user_email_validated = 1
            user.save()
            return Response({'message':"User Validated"}, status = 200)
    
    return Response({'error':'User was not able to be validated'}, status = 400)

@api_view(['POST'])
def request_new_code_view(request):
    user = CustomUser.objects.filter(auth_token=request.auth).first()

    if user.user_email_validated == 1:
        return Response({'error':'This is a validated user'}, status = 400)

    user.user_validation_code = random.randint(100000001, 999999998)
    user.save()

    send_mail(
        subject='WallStreetBeasts Email Verification',
        message=("Hello "+user.username+", your code is "+str(user.user_validation_code)+" please enter this code into the website to be able to validate your account!"),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )

    return Response({'message':'Code Regenerated and Email Resent'}, status = 200)

@api_view(['POST'])
def stocks_data_view(request):
    tickers = request.data.get('tickers')
    stock_data = PortfolioAnalyzer().analyze_stocks(tickers)
    stock_data = make_analyzed_stock_json(stock_data)
    return Response(stock_data, status=200)

def make_analyzed_stock_json(stock_data):
    options = list(stock_data.keys())
    Analyzed_stock_classes = list()
    for option in options:
        for stock in stock_data[option]:
            Analyzed_stock_classes.append(stock)
    super_final_dict = dict()
    for Analyzed_stock_class in Analyzed_stock_classes:
        final_dict = dict()
        recommendation = Analyzed_stock_class.recommendation
        ticker = Analyzed_stock_class.ticker
        score = Analyzed_stock_class.score
        final_dict["ticker"] = ticker
        final_dict["recommendation"] = recommendation
        final_dict["score"] = score
        analysis = Analyzed_stock_class.analysis
        for k, v in analysis.items():
            final_dict[k] = v
        print(final_dict)
        super_final_dict[ticker] = final_dict
    return json.dumps(super_final_dict)
