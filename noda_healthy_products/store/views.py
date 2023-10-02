from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from .forms import UserCreationForm, VerifyForm, LoginForm
from .models import Product, Tag, Order, ConfirmedOrder
from . import verify
from User.models import City
from .decorators import verification_required
# Create your views here.


def base(request):
    return render(request, 'base.html')

def index(request):
    return render(request, 'index.html', {"featured_products": Product.objects.filter(in_the_main_page = True)})

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print('hello1')
        if form.is_valid():
            user = form.save()
            # print(user.id)
            auth.login(request, user)
            # print('hello2')
            # verify.send(form.cleaned_data.get('mobile'))
            # return redirect('/verify')
            return redirect('/')
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

def sendVerifyPage(request):
    return render(request, "sendVerifyPage.html")

def sendVerify(request):
    mobile = request.user.mobile
    verify.send(mobile)
    return redirect('/verify')

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

@login_required
@verification_required
def addToCart(request, to_url, productid, count):
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
    return redirect(f'/{to_url}')

def changeCount(request, from_url, ope, id):
    order = Order.objects.get(id=id)
    if ope == 'add': 
        order.count+=1
        order.price += order.product.price
        request.user.products_in_cart +=1
    elif ope == 'minus':
        order.count-=1
        order.price-=order.product.price
        request.user.products_in_cart -=1
        if order.count == 0:
            order.delete()
            request.user.save()
            return redirect(f'/{from_url}')
    else:
        request.user.products_in_cart -= order.count
        order.delete()
        request.user.save()
        return redirect(f'/{from_url}')
    request.user.save()
    order.save()
    return redirect(f'/{from_url}')

def cart(request):
    orders = Order.objects.filter(user= request.user, is_confirmed=False)
    return render(request, 'cart.html', {"orders": orders, 'orders_exist' : len(orders) > 0 })

def profile(request):
    return render(request, 'profile.html',{"noedit": True, "city": request.user.city })

def editProfile(request, to_url):
    return render(request, 'profile.html',{"noedit":False, "cities": City.objects.all(),'to_url': to_url })

def changeProfile(request, to_url):
    user = request.user
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get("last_name")
    user.city = City.objects.get(id = int(request.POST.get("city")))
    user.address = request.POST.get("address")
    nwMobile = request.POST.get('mobile')
    if user.mobile != nwMobile:
        user.is_verified = False
        user.mobile = nwMobile
    user.save()
    return redirect(f'/{to_url}')

def purchase(request):
    if request.user.products_in_cart < 1: 
        messages.error(request, "لا يوجد اي منتجات فى السله")
        return redirect('/')
    orders = Order.objects.filter(user= request.user, is_confirmed=False)
    return render(request, 'purchase.html', {'orders' : orders})

def pay(request):
    if request.user.products_in_cart < 1: 
        messages.error(request, "لا يوجد اي منتجات فى السله")
        return redirect('/')
    elif request.method == "POST":
        fav = request.POST.get('fav_payment')
        if fav == 'cash':
            sm = 0
            # cnt = 0
            user = request.user
            conf = ConfirmedOrder.objects.create(user=user,mobile=user.mobile,address=user.address,city=user.city)
            for i in Order.objects.filter(user=user, is_confirmed=False):
                i.conf_order = conf
                i.is_confirmed = True
                sm += i.price * i.count
                # cnt += i.count
                i.save()
            conf.price = sm
            user.products_in_cart = 0
            conf.save()
            user.save()
        return redirect('myOrders')
    else: return redirect('/purchace')

def myOrders(request):
    delivered_orders = Order.objects.filter(user=request.user, is_confirmed=True, conf_order__status="delivered").order_by('conf_order')
    not_delivered_orders = Order.objects.filter(Q(user=request.user), Q(is_confirmed=True),Q(conf_order__status="pending") | Q(conf_order__status="shipping")).order_by('conf_order')
    return render(request, 'myOrders.html', {
        'delivered_orders' : delivered_orders,
        'delivered_not_exist' : not delivered_orders.exists(),
        'not_delivered_orders' : not_delivered_orders,
        'not_delivered_not_exist' : not not_delivered_orders.exists()
    })

def myOrder(request):
    return render(request, 'myOrder.html')

# admin views functinos ...
def adminOrders(request, showed):
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
        pend = dict()
        ship = dict()
        deliver = dict()
        for key in d.keys():
            for val in d[key].keys():
                if val.status == 'pending':
                    if key not in pend.keys(): pend[key] = dict()
                    pend[key][val] = d[key][val]
                elif val.status == 'shipping':
                    if key not in ship.keys(): ship[key] = dict()
                    ship[key][val] = d[key][val]
                elif val.status == 'delivered':
                    if key not in deliver.keys(): deliver[key] = dict()
                    deliver[key][val] = d[key][val]
                    
        return render(request, 'adminOrders.html', {"delivered": deliver, "pending": pend, "shipping" : ship, "showed": showed})
    else: return redirect('/')

def changeConfOrderStat(request, to_url, stat, id):
    if not request.user.is_superuser: return redirect('/')
    conf_order = ConfirmedOrder.objects.get(id=id)
    conf_order.status = stat
    conf_order.save()
    return redirect(f'/adminOrders/{to_url}')


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