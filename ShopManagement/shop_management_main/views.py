from django.shortcuts import render, redirect
from .models import Product, TransactionDay
from .forms import ProductForm, TransactionForm

def index(request):
    """The homepage for our app"""
    return render(request, 'index.html')

def products(request):
    """The page that contain all of the products."""
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

def transaction_days(request):
    """Menu to show all transaction days."""
    transaction_days = TransactionDay.objects.all()
    context = {'transaction_days' : transaction_days}
    return render(request, 'transaction_days.html', context)

def new_transaction_day(request):
    """Add a new transaction day if it doesn't exist."""
    count = 0
    day_list = TransactionDay.objects.filter(owner=request.user).all()
    new_day = TransactionDay.objects.create(owner=request.user)
    for item in day_list:
        if item.date == new_day.date:
            count += 1
    if count == 2:
        new_day.delete()
    return redirect('shop_management_main:transaction_days')

def transactions(request, transaction_day_id):
    """A page that shows transactions of a particular day."""
    transaction_day = TransactionDay.objects.get(id=transaction_day_id)
    transactions = transaction_day.transaction_set.all()
    context = {
        'transactions' : transactions,
        'day' : transaction_day
        }
    return render(request, 'transactions.html', context)

def new_transaction(request, transaction_day_id):
    """Adding a new transaction"""
    day = TransactionDay.objects.get(id=transaction_day_id)
    if request.method != 'POST':
        #No data submitted; create a blank form.
        form = TransactionForm()
    else:
        #Post data submitted; process data.
        form = TransactionForm(data=request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.day = day
            new_transaction.save()
            return redirect('shop_management_main:transactions',
                transaction_day_id=transaction_day_id)

    #Display a blank or invalid form.
    context = {
        'form' : form,
        'day' : day
        }
    return render(request, 'new_transaction.html', context)
