from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer
from .models import User

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Only Logged-in users (Admins) can create users
def register_user(request):
    # Ensure only Admins can create users
    if not request.user.is_superuser and request.user.role != User.ADMIN:
        return Response({'error': 'Only Admins can create users'}, status=403)
    
    # Deserialize and validate
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'messsage': 'User created Sucessful'}, status=201)
    
    return Response(serializer.errors, status=400)

# Login User
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login Successful'}, status=200)
    
    return Response({'error': 'Invalid credential'}, status=400)