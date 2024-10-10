from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .forms import CustomAuthenticationForm, ProductForm, BillForm
from .models import Product, Bill,TotalAmount
from django.db import transaction
import math
from . import models
from django.db.models import Sum 
from . import custom_filters

def index(request):
    return HttpResponse("home page")

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def product_list(request):
   
    products = Product.objects.all()

   
    product_totals = {}

    
    bills = Bill.objects.all()
    for bill in bills:
        if bill.product_id not in product_totals:
            product_totals[bill.product_id] = {
                'total_sold': 0
            }
        product_totals[bill.product_id]['total_sold'] += bill.quantity

 
    for product in products:
        if product.product_id in product_totals:
            total_sold = product_totals[product.product_id]['total_sold']
            product.remaining = product.quantity - total_sold
        else:
            product.remaining = product.quantity

    
    low_quantity_products = [product for product in products if product.remaining <= 20]

  
    return render(request, 'product_list.html', {'products': products, 'low_quantity_products': low_quantity_products})



    





def update_product(request, product_id):
    if request.method == 'POST':
        edit_name = request.POST.get('edit_name')
        edit_price = request.POST.get('edit_price')
        edit_quantity = request.POST.get('edit_quantity')

      
        product = get_object_or_404(Product, pk=product_id)

       
        product.name = edit_name
        product.price = edit_price
        product.quantity = edit_quantity
        product.save()

     
        return redirect('product_list')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def bill_list(request):
    bills = Bill.objects.all()
    return render(request, 'bill_list.html', {'bills': bills})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Bill, Product

def add_bill(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

      
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return JsonResponse({'error': 'Quantity must be a positive integer'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity format'}, status=400)

       
        

        
        amount = int(product.price) * quantity

       
        bill = Bill(
            transaction_id=transaction_id,
            product=product,
            quantity=quantity,
            amount=amount
        )
        bill.save()

        return redirect('bill_list')
    else:
        return render(request, 'bill_list.html')


    

def calculate_total_amount(request):
    # Get all distinct transaction IDs from bills
    bills = Bill.objects.all()
    transaction_ids = set(bill.transaction_id for bill in bills)

    # Calculate total amount for each transaction ID and save in TotalAmount table
    for t_id in transaction_ids:
        bills_for_transaction = [bill for bill in bills if bill.transaction_id == t_id]
        total_amount = sum(bill.quantity * bill.product.price for bill in bills_for_transaction)

        # Check if TotalAmount entry exists, if not create new, otherwise update
        try:
            total_amount_obj = TotalAmount.objects.get(transaction_id=t_id)
        except TotalAmount.DoesNotExist:
            total_amount_obj = TotalAmount(transaction_id=t_id)

        total_amount_obj.total_amount = total_amount
        total_amount_obj.save()

    # Retrieve all TotalAmount entries for display
    total_amounts = TotalAmount.objects.all()

    return render(request, 'total_amount_list.html', {'total_amounts': total_amounts})