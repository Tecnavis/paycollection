# from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

# class LoginView(APIView):

#     def post(self, request):
#         phone = request.data.get("phone_number")
#         password = request.data.get("password")

#         if not phone or not password:
#             return Response(
#                 {"detail": "Phone number and password required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user = authenticate(request, username=phone, password=password)

#         if user is None:
#             return Response(
#                 {"detail": "Invalid phone number or password"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

#         refresh = RefreshToken.for_user(user)

#         return Response(
#             {
#                 "message": "Login successful",
#                 "user_id": user.id,
#                 "phone": user.contact_number,
#                 "role": user.role,
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh),
#             },
#             status=status.HTTP_200_OK
#         )


from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):

    def post(self, request):
        phone = request.data.get("phone_number")
        password = request.data.get("password")

        if not phone or not password:
            return Response(
                {"detail": "Phone number and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            contact_number=phone,
            password=password
        )

        if user is None:
            return Response(
                {"detail": "Invalid phone number or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful",
                "user_id": user.id,
                "phone": user.contact_number,
                "role": user.role,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK
        )
