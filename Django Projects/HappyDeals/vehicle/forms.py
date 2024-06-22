from django import forms
from .models import Vehicle
from.models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm



class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'vehicle_type', 'max_persons', 'fuel_efficiency', 'price_per_km', 'availability', 'image_url']

class RentalForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pickup_date', 'return_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_name'] = forms.CharField(max_length=100, initial=self.instance.customer.username)
        self.fields['customer_phone'] = forms.CharField(max_length=15)

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.customer.username = self.cleaned_data['customer_name']
        booking.customer.phone = self.cleaned_data['customer_phone']
        if commit:
            booking.save()
        return booking

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)