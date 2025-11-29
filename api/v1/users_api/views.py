from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import CustomUser, UserRoles
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .serializers import LoginSerializer, UserListSerializer,CustomUserSerializer,UserSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required as admin_required
from main.management.commands.create_roles_and_permissions import IsMainAdmin,IsSecondaryAdmin
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


import logging

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Flexible login endpoint that accepts either `email` or `username`
    plus `password`.
    """
    data = request.data

    # Accept several possible field names from the frontend
    identifier = (
        data.get('email')
        or data.get('username')
        or data.get('user')
        or data.get('login')
        or data.get('email_id')
    )
    password = data.get('password')

    if not identifier or not password:
        return Response(
            {"detail": 'Must include "email" (or "username") and "password".'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Treat identifier as email, since CustomUser authenticates by email
    user = authenticate(email=identifier, password=password)
    print("login_user identifier:", identifier, "=> user:", user)

    if user is None:
        return Response(
            {"detail": "Invalid email or password."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not user.is_active:
        return Response(
            {"detail": "User account is disabled."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    refresh = RefreshToken.for_user(user)

    response_data = {
        'detail': 'Login successful',
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': getattr(user, 'role', None),
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    print(user,"user")
    serializer = UserListSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_profile_by_id(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserListSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsSecondaryAdmin]) 
def create_staff_user(request):
    serializer = CustomUserSerializer(data=request.data)
    
    if serializer.is_valid():
        password = serializer.validated_data.pop('password', None)  
        user = serializer.save(is_staff=True)
        
        if password:
            user.set_password(password)  
            user.save()
        
        return Response(
            {"message": "Staff user created successfully"},
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsSecondaryAdmin | IsMainAdmin])  
def create_admin_user(request):
    serializer = CustomUserSerializer(data=request.data)
    
    if serializer.is_valid():
        password = serializer.validated_data.pop('password', None)  
        
        user = serializer.save(
            role=UserRoles.ADMIN, 
            is_staff=True, 
            is_superuser=False  
        )

        if password:
            user.set_password(password)  
            user.save()
        
        return Response(
            {"message": "Admin user created successfully"},
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_staff_users(request):
    staff_users = CustomUser.objects.filter(is_staff=True)
    serializer = UserListSerializer(staff_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# update staff user
@api_view(['PUT'])
@permission_classes([IsSecondaryAdmin | IsMainAdmin])  
def update_staff_user(request, id):
    try:
        staff_user = CustomUser.objects.get(pk=id)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(staff_user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsSecondaryAdmin | IsMainAdmin])  
def update_admin_user(request, id):
    try:
        staff_user = CustomUser.objects.get(pk=id)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(staff_user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsSecondaryAdmin | IsMainAdmin])  
def delete_staff_user(request, id):
    staff_user = CustomUser.objects.get(pk=id)
    # staff_user.is_deleted = True
    # staff_user.save()
    staff_user.delete() 
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsMainAdmin | IsSecondaryAdmin])  
def delete_admin_user(request, id):
    staff_user = CustomUser.objects.get(pk=id)
    staff_user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    data = request.data
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    
    if not user.check_password(old_password):
        return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)