from django.db import models
from user_mgmt.models import User
from listing.models import Listing

class ApprovalAction(models.TextChoices):
    APPROVE = 'approve', 'Approve'
    REJECT = 'reject', 'Reject'

class Admin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin: {self.user.email}"

class ListingApproval(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='approvals'
    )
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listing_approvals'
    )
    action = models.CharField(
        max_length=10,
        choices=ApprovalAction.choices
    )
    reason = models.TextField(blank=True, null=True)
    approval_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.admin.email} for {self.listing.title}"

    class Meta:
        indexes = [
            models.Index(fields=['approval_date']),
            models.Index(fields=['action']),
        ]

class AlertType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Alert(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    alert_type = models.ForeignKey(
        AlertType,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    description = models.TextField(blank=True, null=True)
    detection_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type.name} for {self.listing.title}"

    class Meta:
        indexes = [
            models.Index(fields=['detection_time']),
        ] 