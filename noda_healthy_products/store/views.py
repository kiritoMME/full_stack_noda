from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserCreationForm, VerifyForm, LoginForm
from . import verify

# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            mobile = form.cleaned_data.get('mobile')
            password = form.cleaned_data.get('password')
            verify.send(mobile)
            auth.authenticate(request, mobile=mobile, password=password)
            return redirect('verify')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        user = auth.authenticate(request, mobile=mobile, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invaid mobile number or password')
    return render(request, 'login.html', {"form": LoginForm() })



@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.mobile, code):
                request.user.is_active = True
                request.user.save()
                return redirect('index')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})
