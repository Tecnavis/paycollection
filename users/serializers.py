# from django.contrib.auth import authenticate
# from rest_framework import serializers

# class PhoneLoginSerializer(serializers.Serializer):
#     contact_number = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(
#             username=data['contact_number'],
#             password=data['password']
#         )

#         if not user:
#             raise serializers.ValidationError("Invalid phone number or password")

#         if not user.is_active:
#             raise serializers.ValidationError("User is inactive")

#         data['user'] = user
#         return data

from django.contrib.auth import authenticate
from rest_framework import serializers

class PhoneLoginSerializer(serializers.Serializer):
    contact_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            contact_number=data["contact_number"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid phone number or password")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        data["user"] = user
        return data
