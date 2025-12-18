from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):

    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")

        if not phone or not password:
            return Response(
                {"error": "Phone number and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=phone, password=password)

        if user is None:
            return Response(
                {"error": "Invalid phone number or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "message": "Login successful",
                "user_id": user.id,
                "phone": user.contact_number,
                "role": user.role
            },
            status=status.HTTP_200_OK
        )
