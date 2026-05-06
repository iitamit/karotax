from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    INCOME_TYPE_CHOICES = [
        ('salaried', 'Salaried Employee'),
        ('freelancer', 'Freelancer / Self-Employed'),
        ('business', 'Business Owner'),
        ('multiple', 'Multiple Income Sources'),
    ]
    phone = models.CharField(max_length=15, blank=True)
    pan_number = models.CharField(max_length=10, blank=True, verbose_name='PAN Number')
    aadhaar_last4 = models.CharField(max_length=4, blank=True, verbose_name='Aadhaar Last 4 Digits')
    income_type = models.CharField(max_length=20, choices=INCOME_TYPE_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    is_profile_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"

    def get_display_name(self):
        return self.get_full_name() or self.username
