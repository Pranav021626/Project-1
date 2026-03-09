from django.shortcuts import render
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


# ✅ HOME PAGE
def home(request):
    return render(request, 'home.html')


# ✅ RESULT PAGE
def result(request):

    if request.method == "POST":

        number = request.POST.get('number')

        try:
            parsed_number = phonenumbers.parse(number)

            country = geocoder.description_for_number(parsed_number, "en")

            sim_carrier = carrier.name_for_number(parsed_number, "en")

            timezones = ", ".join(timezone.time_zones_for_number(parsed_number))

            valid = phonenumbers.is_valid_number(parsed_number)

            context = {
                'number': number,
                'country': country if country else "Not Available",
                'carrier': sim_carrier if sim_carrier else "Not Available",
                'timezone': timezones if timezones else "Not Available",
                'valid': valid
            }

        except:
            context = {
                'number': number,
                'country': "Invalid Number",
                'carrier': "Invalid",
                'timezone': "Invalid",
                'valid': False
            }

        return render(request, 'result.html', context)

    return render(request, 'home.html')


# ✅ ABOUT PAGE
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')



def signup_view(request):

    if request.method == "POST":

        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')

def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def profile(request):
    if request.method == 'POST' and request.FILES.get('image'):
        request.user.profile.image = request.FILES['image']
        request.user.profile.save()
        return redirect('profile')

    return render(request, 'profile.html')  

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    return redirect('profile') 
    
        