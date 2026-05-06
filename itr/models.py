from django.db import models
from django.conf import settings

class ITRFiling(models.Model):
    STATUS_CHOICES = [
        ('draft', 'In Progress'),
        ('review', 'Under Review'),
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
    ]
    REGIME_CHOICES = [
        ('old', 'Old Tax Regime'),
        ('new', 'New Tax Regime'),
        ('ai_recommended', 'AI Recommended'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='itr_filings')
    tax_year = models.CharField(max_length=10, default='2024-25')
    itr_type = models.CharField(max_length=10, default='ITR-1')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    regime = models.CharField(max_length=20, choices=REGIME_CHOICES, default='ai_recommended')
    current_step = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Computed fields (filled by AI)
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxable_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_liability = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refund_or_payable = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ai_regime_suggestion = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'tax_year']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_display_name()} - {self.tax_year} ({self.status})"

    def get_step_percent(self):
        return int((self.current_step / 5) * 100)


class IncomeDetails(models.Model):
    filing = models.OneToOneField(ITRFiling, on_delete=models.CASCADE, related_name='income')
    # Salary
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hra_received = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hra_exemption = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    form16_uploaded = models.BooleanField(default=False)
    # Freelance/Business
    freelance_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    business_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Other Income
    interest_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rental_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital_gains_stcg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital_gains_ltcg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # TDS
    tds_deducted = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    advance_tax_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def total(self):
        return (self.basic_salary + self.other_allowances - self.hra_exemption +
                self.freelance_income + self.business_income + self.interest_income +
                self.rental_income + self.capital_gains_stcg + self.capital_gains_ltcg +
                self.other_income)


class DeductionDetails(models.Model):
    filing = models.OneToOneField(ITRFiling, on_delete=models.CASCADE, related_name='deductions')
    # 80C - Max 1.5L
    ppf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    elss = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    epf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lic_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    home_loan_principal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tuition_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nsc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # 80D - Health Insurance
    health_insurance_self = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    health_insurance_parents = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Other
    nps_80ccd = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='NPS (80CCD)')
    home_loan_interest_24b = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    education_loan_80e = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    donation_80g = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    savings_interest_80tta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    standard_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=50000)

    def section_80c_total(self):
        total = (self.ppf + self.elss + self.epf + self.lic_premium +
                 self.home_loan_principal + self.tuition_fees + self.nsc)
        return min(total, 150000)

    def total(self):
        return (self.section_80c_total() + self.health_insurance_self +
                self.health_insurance_parents + self.nps_80ccd +
                self.home_loan_interest_24b + self.education_loan_80e +
                self.donation_80g + min(self.savings_interest_80tta, 10000) +
                self.standard_deduction)
