from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from customer.models import Customer, CustomerAssignment, Agent
from users.models import CustomUser
from django.contrib.auth.hashers import make_password


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "email", "contact_number", "password", ] 


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "contact_number","password",] 
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"required": False}}  
    def validate_password(self, value):
            """ automatically hashes the password before saving, ensuring it’s stored securely """
            return make_password(value) if value else value

class CustomerSerializer(ModelSerializer):
    user = CustomUserSerializer()  

    class Meta:
        model = Customer
        exclude = ["created_by", "updated_by", "created_at", "updated_at"]
        extra_kwargs = {"user": {"required": False}}

    def create(self, validated_data):
        """Handles creation of Customer & its User"""
        user_data = validated_data.pop("user", None) 
        request = self.context.get("request")

        if user_data:
            user_instance = CustomUser.objects.create(**user_data, role="customer")
        else:
            raise ValueError("User data is required to create a customer")

        validated_data["user"] = user_instance
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
            validated_data["updated_by"] = request.user

        return super().create(validated_data)
    def update(self, instance, validated_data):
        request = self.context.get("request")
        user_data = validated_data.pop("user", None)

        if user_data:
            user_instance = instance.user
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        if request and hasattr(request, "user"):
            validated_data["updated_by"] = request.user

        return super().update(instance, validated_data)

class CustomerListSerializer(ModelSerializer):
    user = UserSerializer()  

    class Meta:
        model = Customer
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['user']


class AgentProfileSerializer(ModelSerializer):
    user = CustomUserSerializer()  

    class Meta:
        model = Agent
        exclude = ["created_by", "updated_by", "created_at", "updated_at"]
        extra_kwargs = {"user": {"required": False}}

    def create(self, validated_data):
        """Handles creation of Agent & its User"""
        user_data = validated_data.pop("user", None) 
        request = self.context.get("request")

        if user_data:
            user_instance = CustomUser.objects.create(**user_data, role="agent")
        else:
            raise ValueError("User data is required to create a agent")

        validated_data["user"] = user_instance
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
            validated_data["updated_by"] = request.user

        return super().create(validated_data)
    def update(self, instance, validated_data):
        request = self.context.get("request")
        user_data = validated_data.pop("user", None)

        if user_data:
            user_instance = instance.user
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        if request and hasattr(request, "user"):
            validated_data["updated_by"] = request.user

        return super().update(instance, validated_data)
    
class AgentListSerializer(ModelSerializer):
    user = UserSerializer()  

    class Meta:
        model = Agent
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        read_only_fields = ['user']


# class AgentProfileSerializer(ModelSerializer):
#     class Meta:
#         model = Agent
#         exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
#         extra_kwargs = {
#             'user': {'required': False},  
#         }
#     def create(self, validated_data):
#         request = self.context.get('request')
#         if request and hasattr(request, "user"):
#             validated_data["created_by"] = request.user
#             validated_data["updated_by"] = request.user
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         request = self.context.get('request')
#         if request and hasattr(request, "user"):
#             validated_data["updated_by"] = request.user
#         return super().update(instance, validated_data)  

# class AgentListSerializer(ModelSerializer):
#     user = UserSerializer()  
#     class Meta:
#         model = Agent
#         exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
#         extra_kwargs = {
#             'user': {'required': False},  
#         }
 
    
class CustomerAssignmentSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    agent = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role="agent"))
    assigned_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False, allow_null=True)

    class Meta:
        model = CustomerAssignment
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data["assigned_by"] = request.user
        return super().create(validated_data)