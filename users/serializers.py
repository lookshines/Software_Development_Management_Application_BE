from rest_framework import serializers
from .models import User, Project

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
        user.save
        return user
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
