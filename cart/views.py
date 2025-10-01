from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from .models import OrderItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def add_to_cart(request, product_id):
    """
    A view to add a product to the cart or update its quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Handle POST with form; otherwise allow GET to add a single item
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        quantity = 1
        update_flag = False
        if form.is_valid():
            cd = form.cleaned_data
            quantity = max(1, cd['quantity'])
            update_flag = cd['update']
        else:
            # Fallback for templates posting a plain quantity value
            try:
                quantity = max(1, int(request.POST.get('quantity', '1')))
            except (TypeError, ValueError):
                quantity = 1
            update_flag = request.POST.get('update', 'False') in ('True', 'true', '1')
    else:
        # GET request: add one unit, no update
        quantity = 1
        update_flag = False
    
    # enforce inventory limit
    if product.inventory <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('cart:cart_detail')
    
    if not update_flag:
        # adding to existing quantity
        current_qty = 0
        product_id_str = str(product.id)
        if product_id_str in cart.cart:
            current_qty = cart.cart[product_id_str]['quantity']
        if current_qty + quantity > product.inventory:
            messages.error(request, 'Requested quantity exceeds available stock.')
            return redirect('cart:cart_detail')
    else:
        # direct set
        if quantity > product.inventory:
            messages.error(request, 'Requested quantity exceeds available stock.')
            return redirect('cart:cart_detail')
    
    # Add to cart
    cart.add(product=product, quantity=quantity, update_quantity=update_flag)
    messages.success(request, f'{product.name} added to cart successfully!')
    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    """
    A view to remove a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    A view to display the cart and its items.
    """
    cart = Cart(request)
    
    # Get product information for cart items
    cart_items = []
    if cart.cart:
        product_ids = list(cart.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}
        
        for product_id, item in cart.cart.items():
            product = product_map.get(product_id)
            if product:
                cart_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'price': float(item['price']),
                    'total_price': float(item['price']) * item['quantity']
                })
    
    # Use mobile-optimized template
    return render(request, 'cart/cart_mobile.html', {'cart': cart, 'cart_items': cart_items})


@login_required
def checkout(request):
    cart = Cart(request)
    
    # Get product information for cart items
    cart_items = []
    if cart.cart:
        product_ids = list(cart.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}
        
        for product_id, item in cart.cart.items():
            product = product_map.get(product_id)
            if product:
                cart_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'price': float(item['price']),
                    'total_price': float(item['price']) * item['quantity']
                })
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # transactional ensure inventory and totals
            with transaction.atomic():
                # refresh products and validate inventory
                product_ids = list(cart.cart.keys())
                products = Product.objects.select_for_update().filter(id__in=product_ids)
                product_map = {str(p.id): p for p in products}
                order_total = 0
                # validate each cart line
                for product_id, item in cart.cart.items():
                    product = product_map.get(product_id)
                    if product is None:
                        messages.error(request, 'One of the products in your cart no longer exists.')
                        return redirect('cart:cart_detail')
                    if item['quantity'] > product.inventory:
                        messages.error(request, f'Not enough stock for {product.name}.')
                        return redirect('cart:cart_detail')
                    line_total = float(item['price']) * item['quantity']
                    order_total += line_total

                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = order_total
                order.save()

                for product_id, item in cart.cart.items():
                    product = product_map[product_id]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=float(item['price']),
                        quantity=item['quantity']
                    )
                # Defer inventory decrement to payment success callback
                # keep cart until payment initiated, then clear
            return redirect(reverse('payments:paystack_initiate', args=[order.id]))
    else:
        form = OrderCreateForm()
    return render(request, 'cart/checkout_mobile.html', {'cart': cart, 'cart_items': cart_items, 'form': form})


def update_cart(request):
    """
    A view to update product quantities in the cart.
    """
    cart = Cart(request)
    if request.method == 'POST' and cart:
        product_ids = cart.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        for product_id in product_ids:
            quantity_key = f'quantity_{product_id}'
            if quantity_key in request.POST and product_id in product_map:
                try:
                    quantity = int(request.POST[quantity_key])
                except (TypeError, ValueError):
                    continue
                quantity = max(0, quantity)
                product = product_map[product_id]
                if quantity == 0:
                    cart.remove(product)
                else:
                    if quantity > product.inventory:
                        messages.error(request, f'Requested quantity for {product.name} exceeds available stock.')
                        quantity = product.inventory
                    cart.add(product, quantity, update_quantity=True)
    return redirect('cart:cart_detail')


def order_success(request):
    """
    A view to show a success message after placing an order.
    """
    return render(request, 'cart/order_success.html')


### 2. Create Cart Logic
