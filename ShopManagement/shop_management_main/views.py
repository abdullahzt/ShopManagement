from django.shortcuts import render, redirect
from .models import Product, TransactionDay
from .forms import ProductForm, TransactionForm, Transaction
from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def index(request):
    """The homepage for our app"""
    return render(request, 'index.html')

@login_required
def products(request):
    """The page that contain all of the products."""
    products = Product.objects.filter(owner=request.user)
    context = {'products' : products}
    return render(request, 'products.html', context)

@login_required
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

@login_required
def transaction_days(request):
    """Menu to show all transaction days."""
    transaction_days = (
        TransactionDay.objects.filter(owner=request.user).order_by('-date'))
    context = {'transaction_days' : transaction_days}
    return render(request, 'transaction_days.html', context)

@login_required
def new_transaction_day(request):
    """Add a new transaction day if it doesn't exist."""
    count = 0
    day_list = TransactionDay.objects.filter(owner=request.user).all()
    #Create new transaction with sum = 0.
    new_day = TransactionDay.objects.create(owner=request.user, sum=0)
    #Checks if day already exist then dont create new.
    for item in day_list:
        if item.date == new_day.date:
            count += 1
    if count == 2:
        new_day.delete()
    return redirect('shop_management_main:transaction_days')

@login_required
def transactions(request, transaction_day_id):
    """A page that shows transactions of a particular day."""
    day = TransactionDay.objects.get(id=transaction_day_id)
    sum = day.sum
    user_check(request, day)
    transactions = day.transaction_set.all()
    context = {
        'transactions' : transactions,
        'day' : day,
        'sum' : sum
        }
    return render(request, 'transactions.html', context)

@login_required
def new_transaction(request, transaction_day_id):
    """Adding a new transaction"""
    day = TransactionDay.objects.get(id=transaction_day_id)
    user_check(request, day)
    if request.method != 'POST':
        #No data submitted; create a blank form.
        form = TransactionForm(user=request.user)
    else:
        #Post data submitted; process data.
        form = TransactionForm(data=request.POST)
        if form.is_valid():
            transactions = day.transaction_set.all()
            new_transaction = form.save(commit=False)
            new_transaction.day = day
            #Update the sum of current transaction day.
            day.sum += new_transaction.product.price * new_transaction.quantity
            day.save()
            #if product is laready sold, just update the quantity.
            for transaction in transactions:
                if transaction.product == new_transaction.product:
                    transaction.quantity += new_transaction.quantity
                    transaction.save()
                    break
            else:
                new_transaction.save()
            return redirect('shop_management_main:transactions',
                transaction_day_id=transaction_day_id)

    #Display a blank or invalid form.
    context = {
        'form' : form,
        'day' : day
        }
    return render(request, 'new_transaction.html', context)

def user_check(request, model):
    """checks if model being requested belong to user"""
    #Ensures user does not access anything by links.
    if model.owner != request.user:
        raise Http404
