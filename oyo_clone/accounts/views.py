from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from utils import *


# Create your views here.
def login_page(request):
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_numeber = request.POST.get('phone_number')
        password = request.POST.get('password')
        hotel_user = HotelUser.objects.filter(
            Q(email = email), Q(password = password)
        )
        if hotel_user.exists():
            messages.warning(request,"User phone number or email already exists")
            return render('account/register')
        hotel_user = HotelUser.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = phone_numeber,
            email = email,
            phone_numeber = phone_numeber,
            email_token = generateRandomToken(),
        )
        hotel_user.set_password('password')
        hotel_user.save()

        sendEmailToken(email,hotel_user.email_token)
        messages.success(request, 'An email sent to verify')
        return redirect('/account/register/')



    return render(request, 'register.html')
