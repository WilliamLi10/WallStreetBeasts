from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from StockData import StockData
from stock_analyzer import StockAnalyzer, StockFormat

# Create your views here.
@api_view(['GET'])
def landing_page(request):
    return Response({'test':'test'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    is_valid = None
    if "@" in username:
        is_valid = authenticate(email=username, password=password)
    else:
        is_valid = authenticate(username=username, password=password)

    if is_valid is None:
        return Response({'error':'Wrong'}, status=400)
    else:
        token = Token.objects.get_or_create(user=is_valid)
        return Response({'token':token.key}, status=200)

@api_view(['POST'])    
def registration_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'message':'Logged Out'}, status=200)