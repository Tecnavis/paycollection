from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from customer.models import Customer, CustomerAssignment, Agent
from users.models import CustomUser
from collectionplans.models import CashCollection,Scheme,CashCollectionEntry


class SchemeSerializer(ModelSerializer):
    class Meta:
        model = Scheme
        fields = "__all__"        


class CashCollectionEntrySerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    scheme_name = serializers.CharField(source="scheme.name", read_only=True)

    class Meta:
        model = CashCollectionEntry
        fields = '__all__'  

    def get_customer_name(self, obj):
        """Fetches customer full name from related CustomUser"""
        if obj.customer and obj.customer.user:
            return f"{obj.customer.user.first_name} {obj.customer.user.last_name}"
        return None


class CashCollectionSerializer(serializers.ModelSerializer):
    scheme_name = serializers.CharField(source='scheme.name', read_only=True)
    customer_name = serializers.SerializerMethodField()    
    scheme_total_amount = serializers.DecimalField(
        source="scheme.total_amount", max_digits=10, decimal_places=2, read_only=True
    )
    
    class Meta:
        model = CashCollection
        fields = ['id', 'scheme', 'scheme_name', 'customer', 'customer_name', 
                  'scheme_total_amount','start_date', 'end_date', 'created_at', 'updated_at']
    
    def get_customer_name(self, obj):
        if hasattr(obj.customer, 'user'):
            user = obj.customer.user
            return f"{user.first_name} {user.last_name}".strip() or user.username
        return "Unknown Customer"


# class CustomerSchemePaymentSerializer(serializers.ModelSerializer):
#     customer_name = serializers.CharField(source="customer.user.first_name", read_only=True)
#     customer_contact = serializers.CharField(source="customer.secondary_contact", read_only=True)
#     scheme_name = serializers.CharField(source="scheme.name", read_only=True)
#     scheme_total_amount = serializers.DecimalField(source="scheme.total_amount", max_digits=10, decimal_places=2, read_only=True)
#     payment_history = serializers.SerializerMethodField()

#     class Meta:
#         model = CashCollectionEntry
#         fields = ["customer_name", "customer_contact", "scheme_name", "scheme_total_amount", "payment_history"]

#     def get_payment_history(self, obj):
#         payments = CashCollectionEntry.objects.filter(customer=obj.customer, scheme=obj.scheme).order_by("created_at")
#         return [
#             {"amount": p.amount, "payment_method": p.payment_method, "date": p.created_at}
#             for p in payments
#         ]

class CustomerSchemePaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.user.first_name", read_only=True)
    customer_contact = serializers.CharField(source="customer.secondary_contact", read_only=True)
    scheme_name = serializers.CharField(source="scheme.name", read_only=True)
    scheme_total_amount = serializers.DecimalField(source="scheme.total_amount", max_digits=10, decimal_places=2, read_only=True)
    payment_history = serializers.SerializerMethodField()

    class Meta:
        model = CashCollectionEntry
        fields = ["customer_name", "customer_contact", "scheme_name", "scheme_total_amount", "payment_history"]

    def get_payment_history(self, obj):
        payments = CashCollectionEntry.objects.filter(customer=obj.customer, scheme=obj.scheme)
        return [{"amount": p.amount, "payment_method": p.payment_method, "date": p.created_at} for p in payments]
