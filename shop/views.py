from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Item
from django.urls import reverse 

from django.db import IntegrityError

from django.contrib.auth import authenticate, login, logout

from .models import Item, Category, Cart

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        items = Item.objects.all()

        try:
            cart = Cart.objects.get(user=request.user)

            cart_items = cart.product.all()

        except Cart.DoesNotExist:
            cart_items = []

        categories = Category.objects.all()

        # Render the index.html template with items and cart_product_ids
        return render(request, "shop/index.html", {
            "items": items,
            "cart" : cart_items,
            "categories": categories,
        })
    
    else:
        return redirect("login")
        


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "shop/login.html", {
                "message" : "Invalid Credentials",
            })
    return render(request, "shop/login.html")

def logout_view(request):
    logout(request)
    return render(request, "shop/login.html", {
        "message" : "Logged Out"
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "shop/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "shop/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "shop/register.html")

# removes product from cart  
def removeCart(request):
    id = request.POST["item_id"]

    cart = Cart.objects.get(user=request.user)
    
    item = Item.objects.get(id=id)

    cart.product.remove(item)

    return HttpResponseRedirect(reverse("index"))

# adds product to cart
def addCart(request):
    id = request.POST["item_id"]

    try:
        cart = Cart.objects.get(user=request.user)
    
        item = Item.objects.get(id=id)

        cart.product.add(item)
    
    except Cart.DoesNotExist:
        cart = Cart(user=request.user)

        cart.save()

        item = Item.objects.get(id=id)

        cart.product.add(item)

    return HttpResponseRedirect(reverse("index"))

@login_required
def cart(request):    
    try:
        cart = Cart.objects.get(user=request.user)

        cart_items = cart.product.all()

        total_price = 0

        for item in cart_items:
            total_price += item.price

    except Cart.DoesNotExist:
        cart_items = []

    return render(request, "shop/cart.html", {
        "items" : cart_items,
        "total_price" : total_price,
        "shipping" : 20,
        "grand_total" : 20 + total_price,
        "count" : len(cart_items)
    })