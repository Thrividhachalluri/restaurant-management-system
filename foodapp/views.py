from django.shortcuts import render, redirect, get_object_or_404
from foodapp.models import FoodItem
from django.contrib import messages
from foodapp.models import Order, OrderItem
from django.db import transaction
import requests

# Create your views here.

def home(request):

    food_items = FoodItem.objects.all()

    # Getting cart items from session
    cart = request.session.get('cart', {})

    # Calculating total cart quantity
    cart_count = sum(cart.values())

    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    api_key = "d31d856162fd4de0a02cfbb33a674279"

    for item in food_items:

        response = requests.get(api_url, params={
            'apiKey': api_key,
            'query': item.food_name,
            'number': 1
        })

        data = response.json()

        if data.get('results'):
            item.api_image = data['results'][0]['image']
        else:
            item.api_image = None

    return render(request, 'home.html', {
        'food_items': food_items,
        'cart_count': cart_count
    })


# Adding to cart
def add_to_cart(request, id):

    cart = request.session.get('cart', {})

    food = get_object_or_404(FoodItem, id=id)

    food_id = str(id)

    if food_id in cart:
        cart[food_id] += 1
    else:
        cart[food_id] = 1

    request.session['cart'] = cart

    messages.success(request, "Item added to cart successfully")

    return redirect('home')


# Displaying cart items
def view_cart(request):

    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for food_id, quantity in cart.items():

        food = get_object_or_404(FoodItem, id=food_id)

        subtotal = food.price * quantity
        total += subtotal

        cart_items.append({
            'food': food,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def payment(request):

        cart = request.session.get('cart', {})

        cart_items = []
        total = 0

        for food_id, quantity in cart.items():
            food = get_object_or_404(FoodItem, id=food_id)

            subtotal = food.price * quantity
            total += subtotal

            cart_items.append({
                'food': food,
                'quantity': quantity,
                'subtotal': subtotal
            })

        if not cart_items:
            messages.warning(request, "Your cart is empty!")
            return redirect('home')

        return render(request, 'payment.html', {
            'cart_items': cart_items,
            'total': total
        })

def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    food_id = str(id)

    if food_id in cart:
        del cart[food_id]

    request.session['cart'] = cart

    messages.success(request, "Item removed from cart!")

    return redirect('cart')

def place_order(request):

    if request.method == 'POST':

        cart = request.session.get('cart', {})

        if not cart:
            messages.warning(request, "Your cart is empty!")
            return redirect('home')

        payment_method = request.POST.get('payment_method')

        if payment_method not in ['COD', 'UPI']:
            messages.error(request, "Select a payment mode.")
            return redirect('payment')

        with transaction.atomic():

            total = 0
            order_items = []

            for food_id, quantity in cart.items():

                food = get_object_or_404(FoodItem, id=food_id)

                subtotal = food.price * quantity
                total += subtotal

                order_items.append((food, quantity))

            order = Order.objects.create(
                payment_method=payment_method,
                total_amount=total
            )

            for food, quantity in order_items:

                OrderItem.objects.create(
                    order=order,
                    food=food,
                    quantity=quantity,
                    price=food.price
                )

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_success', order_id=order.id)

    return redirect('payment')


def order_success(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(request, 'order_success.html', {
        'order': order
    })
