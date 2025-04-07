from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from collectionplans.models import CashCollection,Scheme,CashCollectionEntry
from django.db.models import Sum


class SchemeSerializer(ModelSerializer):
    class Meta:
        model = Scheme
        fields = "__all__"        


class CashCollectionEntrySerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    shop_name = serializers.CharField(source="customer.shop_name", read_only=True)
    scheme_name = serializers.CharField(source="scheme.name", read_only=True)
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = CashCollectionEntry
        fields = '__all__'  

    def get_customer_name(self, obj):
        """Fetches customer full name from related CustomUser"""
        if obj.customer and obj.customer.user:
            return f"{obj.customer.user.first_name} {obj.customer.user.last_name} {obj.customer.shop_name}".strip()
        return None
    
    
    def get_created_by(self, obj):
        """Fetches the name or email of the user who created the entry"""
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.email
        return None


    def get_updated_by(self, obj):
        """Fetches the name or email of the user who last updated the entry"""
        if obj.updated_by:
            return f"{obj.updated_by.first_name} {obj.updated_by.last_name}".strip() or obj.updated_by.email
        return None
    

    def validate(self, data):
        customer = data.get("customer")
        scheme = data.get("scheme")
        new_amount = data.get("amount", 0)

        if not customer or not scheme:
            raise serializers.ValidationError("Customer and scheme are required.")

        total_paid = CashCollectionEntry.objects.filter(
            customer=customer,
            scheme=scheme
        ).aggregate(total=Sum("amount"))["total"] or 0

        scheme_total = scheme.total_amount

        if total_paid + new_amount > scheme_total:
            raise serializers.ValidationError(
                f"Overpayment detected. You've already paid ₹{total_paid}, "
                f"so you can only pay up to ₹{scheme_total - total_paid} more."
            )

        return data


class CashCollectionSerializer(serializers.ModelSerializer):
    scheme_name = serializers.CharField(source='scheme.name', read_only=True)
    customer_details = serializers.SerializerMethodField()    
    scheme_total_amount = serializers.DecimalField(
        source="scheme.total_amount", max_digits=10, decimal_places=2, read_only=True)
    installment_amount = serializers.DecimalField(
        source="scheme.installment_amount", max_digits=10, decimal_places=2, read_only=True)
    total_paid = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    payment_progress = serializers.SerializerMethodField()
    installments_paid = serializers.SerializerMethodField()
    installments_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = CashCollection
        fields = [
            'id', 'scheme', 'scheme_name', 'customer_details', 'customer', 
            'total_paid', 'remaining_amount', 'payment_progress',
            'scheme_total_amount', 'installment_amount', 'installments_paid',
            'installments_remaining', 'created_by', 'updated_by',
            'start_date', 'end_date', 'created_at', 'updated_at'
        ]
    
    def get_customer_details(self, obj):
        if obj.customer:
            customer = obj.customer
            user = customer.user
            return {
                "id": customer.id,
                "profile_id": customer.profile_id,
                "shop_name": customer.shop_name,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "contact_number": user.contact_number,
                "email": user.email,
            }
        return None

    def get_total_paid(self, obj):
        entries = CashCollectionEntry.objects.filter(customer=obj.customer, scheme=obj.scheme)
        return sum(entry.amount for entry in entries)

    def get_remaining_amount(self, obj):
        total_paid = self.get_total_paid(obj)
        return float(obj.scheme.total_amount) - float(total_paid)

    def get_payment_progress(self, obj):
        total_paid = self.get_total_paid(obj)
        if obj.scheme.total_amount == 0:
            return 0
        return round((float(total_paid) / float(obj.scheme.total_amount)) * 100, 2)

    def get_installments_paid(self, obj):
        if not obj.scheme.installment_amount:
            return None
        total_paid = self.get_total_paid(obj)
        return int(float(total_paid) // float(obj.scheme.installment_amount))

    def get_installments_remaining(self, obj):
        if not obj.scheme.installment_amount:
            return None
        total_installments = float(obj.scheme.total_amount) / float(obj.scheme.installment_amount)
        installments_paid = self.get_installments_paid(obj)
        return int(total_installments - installments_paid)


class CustomerSchemePaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.user.first_name", read_only=True)
    scheme_name = serializers.CharField(source="scheme.name", read_only=True)
    scheme_total_amount = serializers.DecimalField(source="scheme.total_amount", max_digits=10, decimal_places=2, read_only=True)
    payment_history = serializers.SerializerMethodField()
    customer_details = serializers.SerializerMethodField() 

    class Meta:
        model = CashCollectionEntry
        fields = ["customer_name", "scheme_name", "scheme_total_amount", "payment_history", "customer_details"]

    def get_payment_history(self, obj):
        payments = CashCollectionEntry.objects.filter(customer=obj.customer, scheme=obj.scheme)
        return [{"amount": p.amount, "payment_method": p.payment_method, "date": p.created_at} for p in payments]
    
    def get_customer_details(self, obj):
        """
        Returns detailed customer info, including user profile data
        """
        if obj.customer:
            customer = obj.customer
            user = customer.user
            return {
                "id": customer.id,
                "profile_id": customer.profile_id,
                "shop_name": customer.shop_name,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "contact_number": user.contact_number,
                "email": user.email,
            }
        return None
