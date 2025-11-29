from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser  # already imported above in your file

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Flexible login endpoint:
    accepts either `email` or `username` (or similar) plus `password`.
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

    if user is None or not user.is_active:
        return Response(
            {"detail": "Invalid email or password."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    refresh = RefreshToken.for_user(user)

    response_data = {
        "detail": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": getattr(user, "role", None),
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

    return Response(response_data, status=status.HTTP_200_OK)
