from django.db import models
from users.models import CustomUser
from customer.models import Customer


class PaymentModes:
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    UPI = "upi"
    CHEQUE = "cheque"

    CHOICES = [
        (CASH, "Cash"),
        (BANK_TRANSFER, "Bank Transfer"),
        (UPI, "UPI"),
        (CHEQUE, "Cheque"),
    ]

class TransactionStatus:
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

    CHOICES = [
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
        (REFUNDED, "Refunded"),
    ]

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True,blank=True)
    scheme = models.ForeignKey('collectionplans.Scheme', on_delete=models.CASCADE,null=True,blank=True, related_name="transactions")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PaymentModes.CHOICES)
    status = models.CharField(max_length=20, choices=TransactionStatus.CHOICES, default=TransactionStatus.PENDING)
    collection_agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="recorded_transactions")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer.user.first_name} - {self.scheme.scheme_name} - {self.amount_paid} ({self.status})"


class TransactionReconciliation(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="reconciliation")
    reconciled_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="reconciled_transactions")
    reconciliation_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Reconciliation for {self.transaction} on {self.reconciliation_date}"


class CashFlow(models.Model):
    balance_type = models.CharField(max_length=50, choices=[("bank", "Bank"), ("hand_cash", "Hand Cash")])
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date = models.DateField(auto_now=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.balance_type} - {self.total_balance} - {self.date}"
    
    class Meta:
        unique_together = ('balance_type', 'date')  