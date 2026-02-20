from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import FoodItem, Cart, Order, OTP

import random


# HOME
def home(request):

    foods = FoodItem.objects.filter(available=True)

    return render(request, "home.html", {"foods": foods})


# ADD TO CART
@login_required
def add_to_cart(request, id):

    food = get_object_or_404(FoodItem, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("/cart/")


# CART PAGE
@login_required
def cart_view(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:

        item.subtotal = item.food.price * item.quantity

        total += item.subtotal

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })


# REMOVE FROM CART
@login_required
def remove_from_cart(request, id):

    item = get_object_or_404(Cart, id=id, user=request.user)

    item.delete()

    return redirect("/cart/")


# PLACE ORDER
@login_required
def place_order(request):

    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:

        Order.objects.create(
            user=request.user,
            food=item.food,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect("/orders/")


# ORDERS PAGE
@login_required
def orders_view(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    for order in orders:

        order.total = order.food.price * order.quantity

    return render(request, "orders.html", {
        "orders": orders
    })


# REGISTER WITH OTP
def register(request):

    if request.method == "POST":

        username = request.POST["username"]

        email = request.POST["email"]

        password = request.POST["password"]

        otp = str(random.randint(100000, 999999))

        OTP.objects.create(email=email, otp=otp)

        send_mail(
            "Smart Canteen OTP",
            f"Your OTP is {otp}",
            "yourgmail@gmail.com",
            [email],
            fail_silently=False,
        )

        request.session["email"] = email
        request.session["username"] = username
        request.session["password"] = password

        return redirect("verify")

    return render(request, "register.html")


# VERIFY OTP
def verify(request):

    if request.method == "POST":

        entered_otp = request.POST["otp"]

        email = request.session.get("email")

        username = request.session.get("username")

        password = request.session.get("password")

        otp_obj = OTP.objects.filter(email=email).last()

        if otp_obj and otp_obj.otp == entered_otp:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return redirect("login")

        else:

            return render(request, "verify.html", {
                "error": "Invalid OTP"
            })

    return render(request, "verify.html")