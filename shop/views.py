from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# ========================= #
#   HOME & AUTHENTICATION   #
# ========================= #

# Render the home page
def homepage(request):
    return render(request, 'home.html')

# Register a new customer and creates an empty cart for the customer
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()                         
            customer = Customer.objects.create(customer=user)
            Cart.objects.create(customer=customer)      
            messages.success(request, 'User registered Successfully!!!')
            return redirect(signin)
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})

# Login user using username & password
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'User logged in successfully!!!')
            return redirect(homepage)
        else:
            messages.warning(request, 'No such user')

    return render(request, 'login.html')

# Logout the currently logged-in user
def signout(request):
    logout(request)
    messages.success(request, 'User logged out successfully!!!')
    return redirect(signin)


# ========================= #
# CATEGORY & PRODUCT VIEWS  #
# ========================= #

# Display all product categories
def categories(request):
    catz = Category.objects.all()
    return render(request, 'catz.html', {'catz': catz})

# Show products belonging to a specific category
def categorywise(request, cid):
    pro = Product.objects.filter(category=cid)
    return render(request, 'cwise.html', {'pro': pro})

# Show all products in random order
def allproducts(request):
    allp = Product.objects.all().order_by('?')
    return render(request, 'allp.html', {'allp': allp})

# Show single product details
def productdetails(request, pid):
    pro = Product.objects.get(id=pid)
    allp = Product.objects.all().order_by('?')[:7]
    return render(request, 'prodetails.html', {'pro': pro, 'allp': allp})


# ========================= #
#   ABOUT / CONTACT PAGE    #
# ========================= #

# Save user enquiry / message
def aboutpage(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect(homepage)

    form = MessageForm()
    return render(request, 'about.html', {'form': form})


# ========================= #
#     PROFILE MANAGEMENT    #
# ========================= #

# Display logged-in user's profile
def profilepage(request):
    user = request.user
    pro = Customer.objects.get(customer=user)
    return render(request, 'profile.html', {'pro': pro})

# Edit customer profile details
def editprofile(request, pid):
    profile = Customer.objects.get(id=pid)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(profilepage)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'editpro.html', {'form': form, 'pro': profile})


            # ======================== #
            #    ADDRESS MANAGEMENT    #
            # ======================== #

# Save a new delivery address for the logged-in customer
def saveaddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.customer = Customer.objects.get(customer=request.user)
            addr.save()
            messages.success(request, 'Address saved Successfully!!')
            return redirect(viewaddress)
    else:
        form = AddressForm()

    return render(request, 'address.html', {'form': form})

# View all saved addresses of the customer 
def viewaddress(request):
    customer = Customer.objects.get(customer=request.user)
    addr = Address.objects.filter(customer=customer)
    count = addr.count()
    return render(request, 'viewaddress.html', {'addr': addr, 'count': count})

# Edit an existing address
def editaddress(request, aid):
    addr = Address.objects.get(id=aid)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=addr)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully')
            return redirect(viewaddress)
    else:
        form = AddressForm(instance=addr)

    return render(request, 'editaddress.html', {'form': form, 'addr': addr})

# Delete an address
def deleteaddress(request, aid):
    addr = Address.objects.get(id=aid)
    if request.method == 'POST':
        addr.delete()
        messages.info(request, 'Address deleted')

    return redirect(viewaddress)


            # ========================= #
            #      CART MANAGEMENT      #
            # ========================= #

# Add product to cart or Buy Now(Increases quantity if item already exists)
@login_required(login_url='/shop/login')
def addtocart(request, pid):
    """

    """
    customer = Customer.objects.get(customer=request.user)
    cart = Cart.objects.get(customer=customer)
    pro = Product.objects.get(id=pid)

    qty = int(request.POST.get('quantity', 1))
    action = request.POST.get('action')

    if action == 'cart':
        item, created = CartItem.objects.get_or_create(cart=cart, product=pro)
        item.quantity = item.quantity + qty if not created else qty
        item.save()
        messages.success(request, 'Item added to the cart')
        return redirect(viewcart)
    elif action == 'buy':
        return redirect(homepage)  # Todo: change to Buy Now page
    return redirect(allproducts)

# Display all cart items
@login_required(login_url='/shop/login')
def viewcart(request):
    customer = Customer.objects.get(customer=request.user)
    cart = Cart.objects.get(customer=customer)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'mycart.html', {'items': items, 'cart': cart})

   
# Update cart item quantity    
@login_required(login_url='/shop/login')
def updatecartItem(request, id, op):
    item = CartItem.objects.get(id=id)

    if op == 'inc':  # inc : increase quantity
        item.quantity += 1
        item.save()
    elif op == 'dec' and item.quantity > 1:  # dec : decrease quantity
        item.quantity -= 1
        item.save()
    else:
        item.delete() # delete if quantity reaches zero
    return redirect(viewcart)

# Remove a single cart item
@login_required(login_url='/shop/login')
def deletecartItem(request, id):
    CartItem.objects.get(id=id).delete()
    return redirect(viewcart)

# Remove all items from cart
def clearcart(request):
    customer = Customer.objects.get(customer=request.user)
    cart = Cart.objects.get(customer=customer)
    CartItem.objects.filter(cart=cart).delete()
    return redirect(viewcart)


            # ========================= #
            #          ORDERS           #
            # ========================= #

# View all orders of the logged-in customer
def vieworders(request):
    customer = Customer.objects.get(customer=request.user)
    order = Order.objects.filter(customer=customer)
    return render(request, 'orders.html', {'order': order})
