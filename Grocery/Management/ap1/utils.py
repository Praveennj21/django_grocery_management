# main/utils.py

from .models import Product, Bill
from django.db.models import Sum

def update_remaining_quantities():
    products = Product.objects.all()

    for product in products:
        quantity_sold = Bill.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0

        # Calculate remaining quantity
        remaining = product.quantity - quantity_sold
        remaining = max(0, remaining)  # Ensure remaining quantity is not negative

        # Update the remaining quantity in the Product model
        product.remaining = remaining
        product.save()

def get_low_quantity_products(threshold=20):
    low_quantity_products = []

    products = Product.objects.all()

    for product in products:
        if product.remaining < threshold:
            low_quantity_products.append({
                'id': product.id,
                'name': product.name,
                'remaining': product.remaining,
            })

    return low_quantity_products
