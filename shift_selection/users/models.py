# models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employer = models.BooleanField(default=False)
    subscription_valid_until = models.DateField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=50, null=True, blank=True)
    is_group_subscription = models.BooleanField(default=False)
    group_subscription_id = models.CharField(max_length=50, null=True, blank=True)
    subscription_enabled = models.BooleanField(default=True)

@receiver(pre_save, sender=UserProfile)
def check_subscription_status(sender, instance, **kwargs):
    # Check subscription status before saving the user profile
    if instance.is_employer and instance.subscription_valid_until and instance.subscription_enabled:
        months_before_notification = 3
        notification_date = instance.subscription_valid_until - timezone.timedelta(days=30 * months_before_notification)

        if timezone.now().date() >= notification_date:
            # Send notification to the employer (you can implement your notification method here)
            send_subscription_notification(instance.user, notification_date)

class Shift(models.Model):
    # Your existing fields
    max_users = models.PositiveIntegerField(default=1)

class Availability(models.Model):
    # Your existing fields
    pass

class Address(models.Model):
    # Your existing fields
    pass

class ShiftOffer(models.Model):
    # Your existing fields
    pass
