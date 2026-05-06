from django.db import models
from django.conf import settings

class FinancialProfile(models.Model):
    RISK_CHOICES = [
        ('conservative', 'Conservative (Safe)'),
        ('moderate', 'Moderate (Balanced)'),
        ('aggressive', 'Aggressive (High Growth)'),
    ]
    GOAL_CHOICES = [
        ('emergency_fund', 'Build Emergency Fund'),
        ('home_purchase', 'Buy a Home'),
        ('retirement', 'Retire Comfortably'),
        ('education', 'Child Education'),
        ('wealth_creation', 'General Wealth Creation'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    existing_savings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    risk_profile = models.CharField(max_length=20, choices=RISK_CHOICES, default='moderate')
    primary_goal = models.CharField(max_length=30, choices=GOAL_CHOICES, default='wealth_creation')
    goal_timeline_years = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def monthly_surplus(self):
        return float(self.monthly_income) - float(self.monthly_expenses)

    def __str__(self):
        return f"{self.user.get_display_name()} - {self.risk_profile}"

class InvestmentRecommendation(models.Model):
    profile = models.ForeignKey(FinancialProfile, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    description = models.TextField()
    suggested_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_return = models.CharField(max_length=50, blank=True)
    risk_level = models.CharField(max_length=20, blank=True)
    tax_benefit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
