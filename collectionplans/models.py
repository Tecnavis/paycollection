from django.db import models
from customer.models import Customer
from users.models import CustomUser
from financials.models import Transaction


class CollectionFrequencyChoices:
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"

    CHOICES = [
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
        (CUSTOM, "Custom"),
    ]

class Scheme(models.Model):
    """Defines the scheme details."""
    scheme_number = models.CharField(max_length=50, unique=True) 
    name = models.CharField(max_length=255, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    collection_frequency = models.CharField(max_length=10, choices=CollectionFrequencyChoices.CHOICES,blank=True, null=True)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_schemes")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="updated_schemes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CashCollection(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True, blank=True, related_name="collections")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cash_collections")
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_collections")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="updated_collections")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.scheme.name} Collection ({self.start_date} - {self.end_date})"
    
class CashCollectionEntry(models.Model):
    """Tracks individual collection transactions for a scheme"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="collection_entries")
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name="scheme_collections", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"), 
        ("bank_transfer", "Bank Transfer"), 
        ("upi", "UPI")
    ]
    
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        default="cash"
    )
    
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_entries")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="updated_entries")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.user.username} - {self.amount}"


class CashFlow(models.Model):
    balance_type = models.CharField(max_length=50, choices=[("bank", "Bank"), ("hand_cash", "Hand Cash")])
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.balance_type} - {self.total_balance}"


class Refund(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE,null=True, blank=True,related_name="refunds")
    amount_refunded = models.DecimalField(max_digits=12, decimal_places=2)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="approved_refunds")
    refund_date = models.DateTimeField(auto_now_add=True)


class CashTransfer(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=10, choices=[('bank', 'Bank'), ('hand', 'Hand Cash')])
    destination = models.CharField(max_length=10, choices=[('bank', 'Bank'), ('hand', 'Hand Cash')])
    transfer_date = models.DateTimeField()
    performed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="cash_transfers")
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source} to {self.destination} - {self.amount} - {self.transfer_date}"
    
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CollectionEntry(models.Model):
    """Model for tracking credit and debit collection entries"""
    
    TYPE_CHOICES = [
        ("credit", "Credit"),
        ("debit", "Debit")
    ]
    
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default="credit"
    )
    
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    narration = models.TextField(blank=True, null=True)
    
    # Tracking fields (unique related_name values to avoid conflicts)
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="created_collection_entries"  # changed here
    )
    updated_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="updated_collection_entries"  # changed here
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Collection Entry"
        verbose_name_plural = "Collection Entries"
    
    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount} on {self.date}"