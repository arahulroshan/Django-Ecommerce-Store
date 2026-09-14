from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .models import Product, Order, OrderItem


# HOME
def home(request):
    products = Product.objects.all()

    return render(
        request,
        'home.html',
        {'products': products}
    )


# LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'login.html',
            {'error': 'Invalid credentials'}
        )

    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')


# REGISTER
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


# PRODUCT DETAILS
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(
        request,
        'product_detail.html',
        {'product': product}
    )


# ADD TO CART
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


# CART
def cart(request):
    cart = request.session.get('cart', {})

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart.get(
            str(product.id),
            0
        )

        item_total = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

        total_price += item_total

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total_price': total_price
        }
    )


# REMOVE FROM CART
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


# INCREASE QUANTITY
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


# DECREASE QUANTITY
def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart and cart[product_id] > 1:
        cart[product_id] -= 1

    request.session['cart'] = cart

    return redirect('cart')


# CHECKOUT
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart.get(
            str(product.id),
            0
        )

        item_total = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

        total_price += item_total

    if request.method == 'POST':

        if not cart_items:
            return redirect('cart')

        order = Order.objects.create(
            user=request.user,
            total_price=total_price
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        request.session['cart'] = {}

        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(
        request,
        'checkout.html',
        {
            'cart_items': cart_items,
            'total_price': total_price
        }
    )


# ORDER SUCCESS
def order_success(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_success.html',
        {'order': order}
    )


# MY ORDERS
def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {'orders': orders}
    )