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
            'contact_number': {'required': True},  # Contact number is required for phone authentication
            'password': {'write_only': True, 'required': False}, 
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)  
        contact_number = validated_data.pop('contact_number')  # Extract contact_number as it's the USERNAME_FIELD
        validated_data['is_staff'] = True  

        # Use create_user to ensure password hashing (contact_number is first argument)
        user = CustomUser.objects.create_user(contact_number, password=password, **validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    # Accept phone number from the client
    phone_number = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    contact_number = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Get phone number from various possible field names
        phone_number = (
            attrs.get('phone_number')
            or attrs.get('phone')
            or attrs.get('contact_number')
            or attrs.get('mobile')
        )
        password = attrs.get('password')

        if not phone_number or not password:
            raise serializers.ValidationError('Must include "phone_number" and "password".')

        # Authenticate by phone number (contact_number is USERNAME_FIELD)
        user = authenticate(username=phone_number, password=password)
        print(user, "user??")

        if not user:
            raise serializers.ValidationError('Invalid phone number or password.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

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
   