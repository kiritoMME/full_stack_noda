from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserCreationForm, VerifyForm, LoginForm
from .models import Product, Tag, Order
from . import verify
from User.models import City
from .decorators import verification_required
# Create your views here.


def base(request):
    return render(request, 'base.html')

@login_required
@verification_required
def index(request):
    return render(request, 'index.html', {"featured_products": Product.objects.filter(in_the_main_page = True)})

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print('hello1')
        if form.is_valid():
            user = form.save()
            print(user.id)
            auth.login(request, user)
            print('hello2')
            verify.send(form.cleaned_data.get('mobile'))
            return redirect('/verify')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form, "cities": City.objects.all()})

def login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        user = auth.authenticate(request, mobile=mobile, password=password)
        print(mobile)
        print(password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invaid mobile number or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.mobile, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('index')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})

def product(request, pk):
    return render(request, 'product.html', {'product': Product.objects.get(id=pk)})

def products(request):
    return render(request, 'products.html', {'products' : Product.objects.all()})

def addToCart(request, productid, count):
    user = request.user
    product = Product.objects.get(id = productid)
    count = int(count)
    try:
        order = Order.objects.get(product = product, user = user)
        order.count += count
        order.price += product.price * count
    except Order.DoesNotExist:
        order = Order.objects.create(user=user, product=product, count=count, price= (product.price * count))
    order.save()
    user.products_in_cart += int(count)
    user.save()
    return redirect('/cart')

def cart(request):
    return render(request, 'cart.html', {"orders": Order.objects.filter(user= request.user)})

def profile(request):
    return render(request, 'profile.html',{"noedit": True, "city": request.user.city })

def editProfile(request):
    return render(request, 'profile.html',{"noedit":False, "cities": City.objects.all() })

def changeProfile(request):
    user = request.user
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get("last_name")
    user.city = City.objects.get(id = int(request.POST.get("city")))
    user.address = request.POST.get("address")
    nwMobile = request.POST.get('mobile')
    if user.mobile != nwMobile:
        user.is_verified = False
        user.mobile = nwMobile
        prvSite = request.META.get('HTTP_REFERER')
        user.save()
        if prvSite != None: return redirect(prvSite)
    user.save()
    return redirect('/profile')

def purchase(request):
    return render(request, 'purchase.html')
