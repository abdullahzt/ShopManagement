from django import forms
from .models import Product, Transaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['text', 'price']
        labels = {
            'text'  : 'Enter product name',
            'price' : 'Enter price'
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'quantity']
        labels = {
            'product' : 'Enter product',
            'quantity' : 'Enter quantity'
        }
