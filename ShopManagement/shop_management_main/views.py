from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

def index(request):
    """The homepage for our app"""
    return render(request, 'index.html')

def products(request):
    """The page that contain all of the products"""
    products = Product.objects.all()
    context = {'products' : products}
    return render(request, 'products.html', context)

def new_product(request):
    """Add a new product."""
    if request.method != 'POST':
        #No data submitted; create a blank form.
        form = ProductForm()
    else:
        #Post data submitted; process data.
        form = ProductForm(data=request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.owner = request.user
            new_product.save()
            return redirect('shop_management_main:products')

    #Display a blank or invalid form.
    context = {'form' : form}
    return render(request, 'new_product.html', context)

def transactions(request):
    """Menu to show all transaction days"""
    transaction_day = TransactionDay.objects.all()
    context = {'products' : products}
    return render(request, 'products.html', context)
