from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['text', 'price']
        labels = {
        'text'  : 'Enter product name',
        'price' : 'Enter price'
        }
