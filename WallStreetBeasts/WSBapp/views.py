from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json

# Create your views here.
@api_view(['GET'])
def landing_page(request):
    return Response({'test':'test'}, status=status.HTTP_200_OK)

