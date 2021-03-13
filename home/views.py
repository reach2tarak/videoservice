from django.shortcuts import render, redirect
from .models import *
import stripe
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.



def home(request):
    courses = Course.objects.all()
    context = {'courses': courses}

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user = request.user).first()
        print(profile)
        request.session['profile'] = profile.is_pro
    return render(request, 'home.html', context)


def view_course(request, slug):
    course = Course.objects.filter(slug = slug).first()
    course_module = CourseModule.objects.filter(course = course)

    context = {'course': course, 'course_module': course_module}
    return render(request, 'course.html', context)

def charge(request):
    return render(request, "charge.html")

def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username)
        print("\n")
        user = User.objects.filter(username=username).first()
        print(user)
        if user is None:
            context = {'message': 'User Does Not Exists'}
            return render(request, 'login.html', context)
        else:
            user = authenticate(username = username, password = password)
            if user is None:
                context = {'message': 'Username/Password Invalid'}
                return render(request, 'login.html', context)
            else:
                login(request, user)
                return redirect('/')

    return render(request, "login.html")



def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")


        user = User.objects.filter(username = username).first()
        if user:
            context = {'message': 'User Already Registered'}
            return render(request, 'register.html', context)
        else:
            user = User(
                username = username,
                email=email
            )
            user.set_password(password)
            user.save()
            context = {'message': 'User Successfully Registered'}
            return render(request, 'register.html', context)

        return render(request, "register.html")

def logout_attempt(request):
    logout(request)
    return redirect('/')


def become_pro(request):
    if request.method == "POST":
        membership = request.POST.get('membership', 'MONTHLY')
        amount = 1000
        if membership == 'YEARLY':
            amount = 11000

        stripe.api_key = 'sk_test_51ITMcGC8w7nHhL7inTcMswyw0TIR7s5KF1NSjXEFQ2LRB54WuMI1IcAprnImmxjCyBCaEMv1oogp7d3juVQoqaGQ00EZEiFfNw'
        customer = stripe.Customer.create(
            email = request.user.email,
            source = request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer = customer,
            amount = amount * 100,
            currency = 'INR',
            description = "Membership"
        )

        if charge['paid'] == True:
            profile = Profile.objects.filter(user = request.user).first()
            if charge['amount'] == 100000:
                profile.subscription_type = 'M'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(30)
                profile.pro_expiry_date = expiry
                profile.save()
            elif charge['amount'] == 1100000:
                profile.subscription_type = 'Y'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(365)
                profile.pro_expiry_date = expiry
                profile.save()
        return redirect('/charge/')

    return render(request, 'become_pro.html')