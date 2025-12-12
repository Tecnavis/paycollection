from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from customer.models import Customer, CustomerAssignment, Agent
from users.models import CustomUser


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
            # Email is optional, phone is mandatory
            "email": {"required": False, "allow_blank": True},
            "contact_number": {"required": True},
        }  
    def validate_password(self, value):
            """ Password validation - don't hash here, let create_user handle it """
            # Return password as-is, create_user will hash it via set_password
            return value

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

        if not user_data:
            raise serializers.ValidationError({"user": ["User data is required to create a customer"]})

        # Extract core auth fields
        password = user_data.pop("password", None)
        contact_number = user_data.pop("contact_number", None)

        if not contact_number:
            raise serializers.ValidationError({"user": {"contact_number": ["Phone number is required"]}})

        # Set role for customer
        user_data["role"] = "customer"
        
        # Handle blank email - set to None if empty string
        if user_data.get("email") == "":
            user_data["email"] = None
        
        try:
            # Create with phone as USERNAME_FIELD (positional argument)
            # Customers can have duplicate phone numbers, so no uniqueness check needed
            user_instance = CustomUser.objects.create_user(
                contact_number,
                password=password,
                **user_data,
            )
        except IntegrityError as e:
            # Handle database constraint errors
            error_message = str(e)
            if "unique" in error_message.lower() or "duplicate" in error_message.lower():
                raise serializers.ValidationError({
                    "user": {"contact_number": ["This phone number already exists for this role."]}
                })
            raise serializers.ValidationError({
                "user": {"contact_number": [f"Database error: {error_message}"]}
            })
        except ValueError as e:
            # Handle validation errors
            raise serializers.ValidationError({
                "user": {"contact_number": [str(e)]}
            })
        except Exception as e:
            # Handle any other errors
            raise serializers.ValidationError({
                "user": {"contact_number": [f"Error creating user: {str(e)}"]}
            })

        validated_data["user"] = user_instance
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
            validated_data["updated_by"] = request.user

        try:
            return super().create(validated_data)
        except Exception as e:
            # If customer creation fails, clean up the user
            user_instance.delete()
            error_message = str(e)
            if "unique" in error_message.lower():
                raise serializers.ValidationError({
                    "profile_id": ["A customer with this profile ID already exists."]
                })
            raise serializers.ValidationError({
                "non_field_errors": [f"Error creating customer: {error_message}"]
            })
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