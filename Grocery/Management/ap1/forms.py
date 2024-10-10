from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Bill

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['transaction_id', 'product', 'quantity']