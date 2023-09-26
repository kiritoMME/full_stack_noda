from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserCreationForm, VerifyForm, LoginForm
from .models import Product, Tag, Order, ConfirmedOrder
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
        order = Order.objects.get(product = product, user = user,is_confirmed = False)
        order.count += count
        order.price += product.price * count
    except Order.DoesNotExist:
        order = Order.objects.create(user=user, product=product, count=count, price= (product.price * count))
    order.save()
    user.products_in_cart += int(count)
    user.save()
    return redirect('/cart')

def cart(request):
    return render(request, 'cart.html', {"orders": Order.objects.filter(user= request.user,is_confirmed=False)})

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

def pay(request):
    if request.method == "POST":
        fav = request.POST.get('fav_payment')
        if fav == 'cash':
            sm = 0
            cnt = 0
            user = request.user
            conf = ConfirmedOrder.objects.create(user=user,mobile=user.mobile,address=user.address,city=user.city)
            for i in Order.objects.filter(user=user):
                i.conf_order = conf
                i.is_confirmed = True
                sm += i.price * i.count
                cnt += i.count
                i.save()
            conf.price = sm
            user.products_in_cart -= cnt
            conf.save()
            user.save()
        return redirect('myOrders')
    else: return redirect('/purchace')

def myOrders(request):
    return render(request, 'orders.html', {'all_orders' : Order.objects.filter(user=request.user, is_confirmed=True).order_by('conf_order')})


# admin views functinos ...
def adminOrders(request):
    if request.user.is_superuser:
        d = dict()
        for i in ConfirmedOrder.objects.all():
            print("welcome............................................................")
            # d[f"{i.user.first_name} {i.user.second_name}"].append(Order.objects.filter(conf_order=i))
            if i.user not in list(d.keys()):
                d[i.user] = dict()
            if i not in list(d[i.user].keys()):
                d[i.user][i] = list()
            d[i.user][i] = Order.objects.filter(conf_order=i)
        return render(request, 'adminOrders.html', {"all_orders": d})
    else: return redirect('/')

def adminConfOrderDetails(request, id):
    if request.user.is_superuser:
        try:
            conf_order = ConfirmedOrder.objects.get(id=int(id))
            return render(request, 'adminConfOrderDetails.html', {
                'conf_order' : conf_order,
                'orders' : Order.objects.filter(conf_order=conf_order)
            })
        except ConfirmedOrder.DoesNotExist:
            messages.error(request, message='ConfirmedOrder.DoesNotExist')
            return redirect('/adminOrders')
    else: return redirect('/')