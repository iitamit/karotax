from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': '10-digit mobile number'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'your@email.com', 'autofocus': True}))

class ProfileSetupForm(forms.ModelForm):
    INCOME_CHOICES = User.INCOME_TYPE_CHOICES
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = User
        fields = ['pan_number', 'aadhaar_last4', 'income_type', 'date_of_birth', 'city', 'state', 'phone']
        widgets = {
            'pan_number': forms.TextInput(attrs={'placeholder': 'ABCDE1234F', 'maxlength': 10, 'style': 'text-transform:uppercase'}),
            'aadhaar_last4': forms.TextInput(attrs={'placeholder': 'Last 4 digits only', 'maxlength': 4}),
        }
