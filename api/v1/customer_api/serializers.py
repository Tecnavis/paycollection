from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from customer.models import Customer, CustomerAssignment, Agent
from users.models import CustomUser



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


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "email", "contact_number"] 
    
class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': False},  
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
            validated_data["updated_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
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
    class Meta:
        model = Agent
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': False},  
        }
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
            validated_data["updated_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data["updated_by"] = request.user
        return super().update(instance, validated_data)  

class AgentListSerializer(ModelSerializer):
    user = UserSerializer()  
    class Meta:
        model = Agent
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': False},  
        }
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
            validated_data["updated_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data["updated_by"] = request.user
        return super().update(instance, validated_data)  
