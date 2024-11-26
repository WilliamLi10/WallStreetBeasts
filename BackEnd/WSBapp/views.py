from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
#from .serializers import CustomUserSerializer
from django.core.mail import send_mail
import random
from django.conf import settings
from .StockRecommendationManager import PortfolioAnalyzer
from .models import CustomUser
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .my_token import gen_token, verify_token, delete_token
from pymongo import MongoClient
from django.contrib.auth.hashers import make_password, check_password
import os
from pathlib import Path
from .news import get_news
from datetime import datetime

# Create your views here.

@api_view(['GET'])
def landing_page(request):
    news = get_news()
    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    collection = database['news-backup']

    if news is None:
        news = collection.find_one()['news']
    else:
        collection.delete_many({})
        collection.insert_one({'news': news, 'date': datetime.now().strftime("%Y%m%d")})
    client.close()

    trending_stocks = None
    json_file_path = os.path.join(os.path.dirname(__file__), 'trending_stocks.json')
    with open(json_file_path, 'r') as json_file:
        trending_stocks = json.load(json_file)

    return Response({'news': news, 'trending_stocks': trending_stocks}, status=status.HTTP_200_OK)

@api_view(['POST'])
def login_view(request):
    print(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    is_valid = None
    if username is None:
        client = MongoClient('localhost', 27017)
        database = client['wsbdb']
        users = database['WSBapp_customuser']
        user = users.find_one({'email': email})
        username = user['username']

    print(username)

    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    users = database['WSBapp_customuser']
    user = users.find_one({'username': username})
    hashed_password = user['password']
    theme = user['theme']
    if theme == 0:
        theme = 'light'
    else:
        theme = 'dark'

    is_valid = check_password(password, hashed_password)

    print(is_valid)

    if not is_valid:
        client.close()
        return Response({'error':'Wrong'}, status=400)
    else:
        token = gen_token(username)
        client.close()
        return Response({'token':token, 'theme':token}, status=200)

@api_view(['POST'])    
def registration_view(request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password = make_password(password)
        code = random.randint(100000001, 999999998)
        user_email_validated = 0
        theme = 1
        newsletter_freq = 1
        phone_number = ""
        risk_pref = 0
        portfolio = ""
        
        userid=0
        with open('WSBapp/userid.txt', 'r') as f:
            userid = f.read().strip()
            userid = int(userid)

        with open('WSBapp/userid.txt', 'w') as f:
            f.write(str(userid+1))

        user_data = {
            'id': userid,
            'username': username,
            'email': email,
            'password': password,
            'user_email_validated': user_email_validated,
            'user_validation_code': code,
            'theme': theme,
            'newsletter_freq': newsletter_freq,
            'phone_number': phone_number,
            'risk_pref': risk_pref,
            'portfolio': portfolio
        }

        client = MongoClient('localhost', 27017)
        database = client['wsbdb']
        users = database['WSBapp_customuser']

        if users.find_one({'username': username}) is not None:
            return Response({'error':'Username already exists'}, status=400)

        if users.find_one({'email': email}) is not None:
            return Response({'error':'Email already exists'}, status=400)

        users.insert_one(user_data)
        client.close()

        send_mail(
            subject='WallStreetBeasts Email Verification',
            message=("Hello "+user_data['username']+", your code is "+str(code)+" please enter this code into the website to be able to validate your account!"),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_data['email']],
            fail_silently=False
        )

        return Response({'username':username, 'password':request.data.get('password'), 'email':email, 'message':'Successfully registered. Use the login information to login.'}, status=200)

@api_view(['POST']) 
def logout_view(request):
    provided_token = request.data.get('token')
    if not provided_token:
        return Response({'error': 'Token Not Provided'}, status=400)

    print(provided_token)

    token = verify_token(provided_token)
    print(token)
    if token is None:
        return Response({'error': 'Bad Token'}, status=401)
    else:
        delete_token(provided_token)
        return Response({'message': 'Logged Out'}, status=200)

@api_view(['POST'])
def verify_email_view(request):
    token = request.data.get('token')
    username = verify_token(token)
    if username is None:
        return Response({'error':'Bad Token'}, status=401)
    
    input_code = int(request.data.get('user_validation_code'))
    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    users = database['WSBapp_customuser']
    user = users.find_one({'username': username})
    actual_code = user['user_validation_code']
    print(input_code)
    print(actual_code)
    if input_code == actual_code:
            users.update_one({'username': username}, {'$set': {'user_email_validated': 1}})
            client.close()
            return Response({'message':"User Validated"}, status = 200)
    
    client.close()
    return Response({'error':'User was not able to be validated'}, status = 400)

@api_view(['POST'])
def request_new_code_view(request):
    token = request.data.get('token')
    username = verify_token(token)

    if username is None:
        return Response({'error':'Bad Token'}, status=401)
    
    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    users = database['WSBapp_customuser']
    user = users.find_one({'username': username})
    new_code = random.randint(100000001, 999999998)
    users.update_one({'username': username}, {'$set': {'user_validation_code': new_code}})

    send_mail(
        subject='WallStreetBeasts Email Verification',
        message=("Hello "+username+", your code is "+str(new_code)+" please enter this code into the website to be able to validate your account!"),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )

    client.close()
    return Response({'message':'Code Regenerated and Email Resent'}, status = 200)

@api_view(['POST'])
def reset_password_view(request):
    email = request.data.get('email')

    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    users = database['WSBapp_customuser']
    user = users.find_one({'email': email})
    if user is None:
        return Response({'error':'Email not found'}, status=400)
    if user['user_email_validated'] == 0:
        return Response({'error':'Email not validated'}, status=400)
    
    new_password = random_password_generator()
    new_password_hashed = make_password(new_password)
    users.update({'email': email}, {'$set': {'password': new_password_hashed}})

    send_mail(
        subject='WallStreetBeasts Password Reset',
        message=("Hello "+user['username']+", your new password is "+new_password+" please enter this password into the website to be able to login!"),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )

    client.close()
    return Response({'message':'Password Reset and Email Sent'}, status=200)

@api_view(['POST'])
def stocks_data_view(request):
    tickers = request.data.get('tickers')
    stock_data = PortfolioAnalyzer().analyze_stocks(tickers)
    stock_data = make_analyzed_stock_json(stock_data)
    return Response(stock_data, status=200)

@api_view(['POST'])
def edit_portfolio_view(request):
    add = request.data.get('add')
    remove = request.data.get('remove')
    token = request.data.get('token')
    username = verify_token(token)
    if username is None:
        return Response({'error':'Bad Token'}, status=401)
    else:
        client = MongoClient('localhost', 27017)
        database = client['wsbdb']
        users = database['WSBapp_customuser']
        user = users.find_one({'username': username})
        portfolio = user['portfolio']
        portfolio = portfolio.split()
        portfolio = set(portfolio)
        for i in add:
            portfolio.add(i)
        for i in remove:
            portfolio.remove(i)
        portfolio = list(portfolio)
        portfolio_string = ""
        for i in range(len(portfolio)):
            if i == len(portfolio)-1:
                portfolio_string += portfolio[i]
            else:
                portfolio_string += portfolio[i] + " "
        users.update_one({'username': username}, {'$set': {'portfolio': portfolio_string}})
        client.close()
        return Response({'message':'Portfolio Updated', 'portfolio':portfolio}, status=200)
    
@api_view(['POST'])
def get_portfolio_view(request):
    token = request.data.get('token')
    username = verify_token(token)
    if username is None:
        return Response({'error':'Bad Token'}, status=401)
    else:
        client = MongoClient('localhost', 27017)
        database = client['wsbdb']
        users = database['WSBapp_customuser']
        user = users.find_one({'username': username})
        portfolio = user['portfolio']
        portfolio = portfolio.split()
        client.close()
        return Response({'portfolio':portfolio}, status=200)

@api_view(['POST'])
def change_email_view(request):
    email = request.data.get('email')
    token = request.data.get('token')

    username = verify_token(token)
    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    users = database['WSBapp_customuser']
    user = users.find_one({'username': username})
    verified = user['user_email_validated']
    if verified == 0:
        client.close()
        return Response({'error':'Email not validated'}, status=400)
    old = user['email']
    users.update_one({'username': username}, {'$set': {'email': email}})
    user = users.find_one({'email': old})
    if user != None:
        users.update_one({'username': username}, {'$set': {'email': old}})
        client.close()
        return Response({'error':'Email already exists'}, status=400)
    client.close()
    return Response({'message':'Email Updated', 'new_email':email, 'old_email':old}, status=200)

@api_view(['POST'])
def change_password_view(request):
    password = request.data.get('password')
    token = request.data.get('token')

    username = verify_token(token)
    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    users = database['WSBapp_customuser']
    user = users.find_one({'username': username})
    verified = user['user_email_validated']
    if verified == 0:
        client.close()
        return Response({'error':'Email not validated'}, status=400)
    hashed_password = make_password(password)
    users.update_one({'username': username}, {'$set': {'password': hashed_password}})
    client.close()
    return Response({'message':'Password Updated'}, status=200)

@api_view(['POST'])
def change_theme_view(request):
    theme = request.data.get('theme')
    token = request.data.get('token')

    if theme == 'light':
        theme = 0
    else:
        theme = 1

    username = verify_token(token)
    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    users = database['WSBapp_customuser']
    users.update_one({'username': username}, {'$set': {'theme': theme}})
    client.close()
    return Response({'message':'Theme Updated', 'theme':theme}, status=200)

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

def random_password_generator():
    password = ""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(16):
        letter_or_number = random.randint(0, 1)
        if letter_or_number == 0:
            password += str(random.randint(0, 9))
        else:
            password += letters[random.randint(0, 25)]
    return password