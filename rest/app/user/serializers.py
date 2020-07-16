from rest_framework import serializers
from rest.app.profile.models import UserProfile
from rest.app.user.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings

"""
How to manage the payload and the encode
"""
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone_number', 'host')


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserSerializer(required = False)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}
    
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user = user,
            first_name = profile_data['first_name'],
            last_name = profile_data['last_name'],
            phone_number = profile_data['phone_number'],
            host = profile_data['host']
        )
        return user

"""
Custome validate method to validate the user and return the token.
If the user is not authenticated or does not exist, it raises an error
"""
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length = 128, write_only = True)
    token = serializers.CharField(max_length = 255, read_only = True)
    
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email = email, password = password)
        
        if user is None:
            raise serializers.ValidationError(
                'The user with this email and password is not found on database'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializer.ValidationError(
                'The user with this email and password does not exist'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }