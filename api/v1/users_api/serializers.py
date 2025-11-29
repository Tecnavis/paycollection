from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import authenticate


CustomUser = get_user_model() 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'contact_number', 'is_staff', 'is_active', 'password']
        extra_kwargs = {
            'is_staff': {'read_only': True},
            'is_active': {'required': False},
            # 'password': {'write_only': True} 
            'password': {'write_only': True, 'required': False}, 
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)  
        validated_data['is_staff'] = True  

        # Use create_user to ensure password hashing
        user = CustomUser.objects.create_user(**validated_data)  

        if password:
            user.set_password(password)  # Hash password
            user.save()

        return user


class LoginSerializer(serializers.Serializer):
    # Accept either `email` or `username` from the client for flexibility
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Support both payload styles:
        # 1) { "email": "...", "password": "..." }
        # 2) { "username": "...", "password": "..." }  (frontend may label the field "email")
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        # If only username was sent, treat it as email for authentication
        if not email and username:
            email = username

        if email and password:
            user = authenticate(email=email, password=password)
            print(user, "user??")

            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Must include "email" (or "username") and "password".')

        attrs['user'] = user
        return attrs

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','role','is_active','is_staff','date_joined','contact_number']
        read_only_fields = ['id','date_joined']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','role','is_active','is_staff','date_joined','contact_number']
        read_only_fields = ['id','date_joined']
   