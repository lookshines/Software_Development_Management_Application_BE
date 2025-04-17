from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','role'] # Fields to accept in API
        extra_kwargs = {'password': {'write_only': True}} # Hide password in response
        
    def create(self, validated_data):
        # Create a new user
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        
        # Hash the password before saving
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'website', 'github_link', 'linkedin_link']
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password_confirmation = serializers.CharField(write_only=True, required=True)
    
    def validate_old_password(self, value):
        user =self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirmation']:
            raise serializers.ValidationError({"new_password_confirmation": "Passwords do not match"})
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        # check if the email exist in the system
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value
    
class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True , validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "password do not match."})
        return data
    
class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()  # Handle missing profiles safely
    
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'is_active', 'profile']
        
    def get_profile(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return UserProfileSerializer(obj.profile).data
        return None
