from django.db import models
from django.core.validators import MinValueValidator
from user_mgmt.models import User
from listing.models import Listing

class TransactionStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'

class TransactionType(models.TextChoices):
    DEPOSIT = 'deposit', 'Deposit'
    PAYMENT = 'payment', 'Payment'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=20)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.amount}"

    class Meta:
        indexes = [
            models.Index(fields=['transaction_date']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_type']),
        ] 