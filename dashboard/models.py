from django.db import models
from users.models import CustomUser
from customer.models import Customer
from collectionplans.models import CashCollectionScheme

class PaymentSchedule(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="payment_schedules")
    scheme = models.ForeignKey(CashCollectionScheme, on_delete=models.CASCADE, related_name="payment_schedules")
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('upcoming', 'Upcoming'),
        ('due', 'Due Today'),
        ('overdue', 'Overdue'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
    ], default='upcoming')
    actual_payment_date = models.DateField(null=True, blank=True)
    transaction = models.ForeignKey('financials.Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name="schedule_item")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer} - {self.scheme.scheme_name} - {self.due_date} - {self.status}"

class AgentCollectionTarget(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="collection_targets", 
                            limit_choices_to={'role': 'agent'})
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    achieved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.agent.first_name} - Target: {self.target_amount} - Achieved: {self.achieved_amount}"
    
    @property
    def achievement_percentage(self):
        if self.target_amount > 0:
            return (self.achieved_amount / self.target_amount) * 100
        return 0

class Report(models.Model):
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=[
        ('monthly', 'Monthly Report'),
        ('weekly', 'Weekly Report'),
        ('daily', 'Daily Report'),
        ('custom', 'Custom Report'),
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    generated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="generated_reports")
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    data = models.JSONField(null=True, blank=True)  # For storing report data directly
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.report_type} - {self.start_date} to {self.end_date}"
    

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('payment_due', 'Payment Due'),
        ('payment_overdue', 'Payment Overdue'),
        ('large_transaction', 'Large Transaction'),
        ('bank_deposit', 'Bank Deposit'),
        ('hand_cash_update', 'Hand Cash Update'),
        ('system', 'System Notification'),
    ])
    is_read = models.BooleanField(default=False)
    related_to = models.CharField(max_length=50, blank=True, null=True)  # Model name
    related_id = models.IntegerField(blank=True, null=True)  # Record ID
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.title} - {self.created_at}"    
    



# class Notification(models.Model):
#     """System notifications and alerts"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     NOTIFICATION_TYPE = [
#         ('payment_due', 'Payment Due'),
#         ('payment_overdue', 'Payment Overdue'),
#         ('payment_received', 'Payment Received'),
#         ('large_transaction', 'Large Transaction'),
#         ('bank_deposit', 'Bank Deposit'),
#         ('hand_cash_update', 'Hand Cash Update'),
#         ('system', 'System Notification'),
#     ]
#     notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
#     title = models.CharField(max_length=100)
#     message = models.TextField()
#     related_payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
#     related_cashflow = models.ForeignKey(CashFlow, on_delete=models.SET_NULL, null=True, blank=True)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.title} - {self.is_read}"

# class AuditLog(models.Model):
#     """Audit trail for all system activities"""
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
#     action = models.CharField(max_length=100)
#     model_name = models.CharField(max_length=100)
#     record_id = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     ip_address = models.GenericIPAddressField(null=True, blank=True)
#     user_agent = models.TextField(blank=True)
#     old_values = models.JSONField(null=True, blank=True)
#     new_values = models.JSONField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.action} - {self.model_name} - {self.timestamp}"


# Add these to your models.py files or create new ones as needed

# For tracking payment schedules and due dates


# class PaymentSchedule(models.Model):
#     customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name="payment_schedules")
#     scheme = models.ForeignKey('collectionplans.CashCollectionScheme', on_delete=models.CASCADE, related_name="payment_schedules")
#     due_date = models.DateField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=[
#         ('upcoming', 'Upcoming'),
#         ('due', 'Due Today'),
#         ('overdue', 'Overdue'),
#         ('paid', 'Paid'),
#         ('partially_paid', 'Partially Paid'),
#     ], default='upcoming')
#     actual_payment_date = models.DateField(null=True, blank=True)
#     transaction = models.ForeignKey('financials.Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name="schedule_item")
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.customer} - {self.scheme.scheme_name} - {self.due_date} - {self.status}"

# # For capturing agent collection targets and tracking
# class AgentCollectionTarget(models.Model):
#     agent = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="collection_targets", 
#                             limit_choices_to={'role': 'agent'})
#     target_amount = models.DecimalField(max_digits=12, decimal_places=2)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     achieved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.agent.first_name} - Target: {self.target_amount} - Achieved: {self.achieved_amount}"
    
#     @property
#     def achievement_percentage(self):
#         if self.target_amount > 0:
#             return (self.achieved_amount / self.target_amount) * 100
#         return 0

# # For tracking cash movements between bank and hand cash
# class CashTransfer(models.Model):
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     source = models.CharField(max_length=10, choices=[('bank', 'Bank'), ('hand', 'Hand Cash')])
#     destination = models.CharField(max_length=10, choices=[('bank', 'Bank'), ('hand', 'Hand Cash')])
#     transfer_date = models.DateTimeField()
#     performed_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name="cash_transfers")
#     notes = models.TextField(blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.source} to {self.destination} - {self.amount} - {self.transfer_date}"

# # For audit logging
# class AuditLog(models.Model):
#     user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name="audit_logs")
#     action = models.CharField(max_length=100)
#     model_name = models.CharField(max_length=100)
#     record_id = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     ip_address = models.GenericIPAddressField(null=True, blank=True)
#     old_values = models.JSONField(null=True, blank=True)
#     new_values = models.JSONField(null=True, blank=True)
    
#     def __str__(self):
#         return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"

# # For notifications
# class Notification(models.Model):
#     user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="notifications")
#     title = models.CharField(max_length=100)
#     message = models.TextField()
#     notification_type = models.CharField(max_length=50, choices=[
#         ('payment_due', 'Payment Due'),
#         ('payment_overdue', 'Payment Overdue'),
#         ('large_transaction', 'Large Transaction'),
#         ('bank_deposit', 'Bank Deposit'),
#         ('hand_cash_update', 'Hand Cash Update'),
#         ('system', 'System Notification'),
#     ])
#     is_read = models.BooleanField(default=False)
#     related_to = models.CharField(max_length=50, blank=True, null=True)  # Model name
#     related_id = models.IntegerField(blank=True, null=True)  # Record ID
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.user} - {self.title} - {self.created_at}"

# # For tracking monthly/weekly reports
# class Report(models.Model):
#     title = models.CharField(max_length=255)
#     report_type = models.CharField(max_length=50, choices=[
#         ('monthly', 'Monthly Report'),
#         ('weekly', 'Weekly Report'),
#         ('daily', 'Daily Report'),
#         ('custom', 'Custom Report'),
#     ])
#     start_date = models.DateField()
#     end_date = models.DateField()
#     generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name="generated_reports")
#     file = models.FileField(upload_to='reports/', null=True, blank=True)
#     data = models.JSONField(null=True, blank=True)  # For storing report data directly
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.title} - {self.report_type} - {self.start_date} to {self.end_date}"
#     