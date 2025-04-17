from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.shortcuts import get_object_or_404

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

# Create Project
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    if not request.user.is_superuser and request.user.role != User.ADMIN:
        return Response({'error': 'Only Admins can create users'}, status=403)
    
    #API for creating a new project.
    
    serializer = ProjectSerializer(data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Project created successfully', 'project':serializer.data}, status=201)
    
    return Response(serializer.errors, status=400)

# Update Profile
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    #API to allow users to update their profile
    
    user = request.user # Get the logged in user
    
    profile, created = UserProfile.objects.get_or_create(user=user)
    serializer = UserProfileSerializer(profile, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile updated successfully', 'profile': serializer.data}, status=200)
    
    return Response(serializer.errors, status=400)

# Change Password
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data, context={'request' : request})
    
    if serializer.is_valid():
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "Password changed successfully!"}, status=200)
    
    return Response(serializer.errors, status=400)

# Request Password Reset
@api_view(['POST'])
def request_password_reset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data('email')
        user = User.objects.get(email=email)
        
        # Generate token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        reset_link = f"{settings.FRONTENDurl}/reset-password/{uid}.{token}/"
        
        # Send reset email
        send_mail(
           "Password Reset Request",
            f"Click here to reset your password: {reset_link}",
            "noreply@example.com",
            fail_silently=False,    
        )
        
        return Response({'message': 'Password reset link sent'}, status = 200)
    
    return Response(serializer.errors, status=400)

# Reset Password
@api_view(['POST'])
def reset_password(request, uidb64, token):
    
    if serializer.is_valid():
        try:
            uid =force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk-uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Invalid reset link'}, status=400)
        
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=400)
        
        # Set new password
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        return Response({'message': 'Password reset successful'}, status=200)
    
    return Response(serializer.errors, status=400)



# Delect User
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    # Only Admins and Superuser can delete users:
    if not request.user.is_superuser and request.user.role != User.ADMIN:
        return Response({"error": "Only Admins can delete users"}, status=403)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=403)
    
    user.delete()
    return Response({'message': 'User deleted Successfully'}, status=200)

# Deactivate User
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def deactivate_user(request, user_id):
    # Only Admins and Superuser can delete users:
    if not request.user.is_superuser and request.user.role != User.ADMIN:
        return Response({"error": "Only Admins can deactivate users"}, status=403)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=403)
    
    user.is_active = False
    user.save()
    return Response({'message': 'User deactivated Successfully'}, status=200)

# Reactivate User
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def reactivate_user(request, user_id):
    # Only Admins and Superuser can delete users:
    if not request.user.is_superuser and request.user.role != User.ADMIN:
        return Response({"error": "Only Admins can reactivate users"}, status=403)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=403)
    
    user.is_active = True
    user.save()
    return Response({'message': 'User reactivated Successfully'}, status=200)

# Get all user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    # Only Admins and Superuser can delete users:
    if not request.user.is_superuser and request.user.role != User.ADMIN:
        return Response({"error": "Only Admins can get users"}, status=403)
    
    users = User.objects.all()
    
    # Serialize user data (conver from database format to JSON)
    serializer = UserSerializer(users, many=True)
    
    # Return response with serilized data
    return Response(serializer.data, status=200)

# Get a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    # Only Admins and Superuser can delete users:
    if not request.user.is_superuser and request.user.role != User.ADMIN:
        return Response({"error": "Only Admins can get user"}, status=403)
    
    user = get_object_or_404(User, id=id)
    
    # Serialize user data (conver from database format to JSON)
    serializer = UserSerializer(user)
    
    # Return response with serilized data
    return Response(serializer.data, status=200)