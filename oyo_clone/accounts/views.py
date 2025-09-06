from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from .utils import *
from django.contrib.auth import authenticate,login,logout
import random
from django.contrib.auth.decorators import login_required




def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        hotel_user = HotelUser.objects.filter(
            Q(email = email), Q(phone_number = phone_number)
        )
        if hotel_user.exists():
            messages.warning(request,"User phone number or email already exists")
            return redirect('/account/register/')
        hotel_user = HotelUser.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = phone_number,
            email = email,
            phone_number = phone_number,
            email_token = generateRandomToken(),
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email,hotel_user.email_token)
        messages.success(request, 'An email sent to verify')
        return redirect('/account/register/')
    return render(request, 'register.html')


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email = email)

        if not hotel_user.exists():
            messages.warning(request,'Account Not Found')
            return redirect('/account/login/')

        if not hotel_user[0].is_verified:
            messages.warning(request, 'Gmail not verified')
            return redirect('/account/login/')

        print(f'{hotel_user[0].username},{password}')
        hotel_user = authenticate(username = hotel_user[0].username, password = password)
        if hotel_user:
            messages.success(request, 'Login Success')
            login(request,hotel_user)
            return redirect('/account/login/')

        messages.warning(request, 'Invalid Credentials')
        return redirect('/account/login/')
    return render(request, 'login.html')

## email varification       

def verifY_email_token(request, token):
    try:
        hotel_user = HotelUser.objects.get(email_token = token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, 'email verified')
        return redirect('/account/login/')
    except HotelUser.DoesNotExist:
        return HttpResponse('Invalid token')
    

def send_otp(request, email):
    hotel_user = HotelUser.objects.filter(email = email)
    if not hotel_user.exists():
        messages.warning(request, 'Account Not Found')
        return redirect('/account/login/')
    
    otp = random.randint(1000,9999)
    hotel_user.update(otp = otp)
    sendOTPtoEmail(email, otp)
    return redirect(f'/account/verify-otp/{email}')


def verify_otp(request, email):
    if request.method == "POST":
        otp = request.POST.get('otp')
        hotel_user = HotelUser.objects.get(email = email)
        
        if otp == hotel_user.otp:
            messages.success(request, 'Login Success')
            login(request,hotel_user)
            return redirect('/account/login')
        messages.warning(request, 'Wrong Otp')
        return redirect(f'/account/verify-otp/{email}')
    return render(request, 'verify_otp.html')


def login_vendor(request):    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelVendor.objects.filter(
            email = email)


        if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/account/login-vendor/')

        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('/account/login-vendor/')

        hotel_user = authenticate(username = hotel_user[0].username , password=password)

        if hotel_user:
            messages.success(request, "Login Success")
            login(request , hotel_user)
            return redirect('/account/dashboard/')

        messages.warning(request, "Invalid credentials")
        return redirect('/account/login-vendor/')
    return render(request, 'vendor/login_vendor.html')

def register_vendor(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')

        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(
            Q(email = email) | Q(phone_number  = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account exists with Email or Phone Number.")
            return redirect('/account/register-vendor/')

        hotel_user = HotelVendor.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            business_name = business_name,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email , hotel_user.email_token)

        messages.success(request, "An email Sent to your Email")
        return redirect('/account/register-vendor/')


    return render(request, 'vendor/register_vendor.html')

def verifY_email_token(request, token):
    try:
        hotel_vendor = HotelVendor.objects.get(email_token = token)
        hotel_vendor.is_verified = True
        hotel_vendor.save()
        messages.success(request, 'email verified')
        return redirect('/account/login-vendor/')
    except HotelUser.DoesNotExist:
        return HttpResponse('Invalid token')

@login_required(login_url = 'login_vendor')
def dashboard(request):
    hotels = Hotel.objects.filter(hotel_owner = request.user)
    context = {'hotels': hotels}
    return render(request, 'vendor/vendor_dashboard.html',context)

def send_otp(request, email):
    hotel_vendor = HotelVendor.objects.filter(email = email)
    if not hotel_vendor.exists():
        messages.warning(request, 'Account Not Found')
        return redirect('/account/login_vendor/')
    
    otp = random.randint(1000,9999)
    hotel_vendor.update(otp = otp)
    sendOTPtoEmail(email, otp)
    return redirect(f'/account/verify-otp/{email}')


def verify_otp(request, email):
    if request.method == "POST":
        otp = request.POST.get('otp')
        hotel_vendor = HotelVendor.objects.get(email = email)
        
        if otp == hotel_vendor.otp:
            messages.success(request, 'Vendor Login Success')
            login(request,hotel_vendor)
            return redirect('/account/login_vendor')
        messages.warning(request, 'Wrong Otp')
        return redirect(f'/account/verify-otp/{email}')
    return render(request, 'verify_otp.html')


# views.py
@login_required(login_url='login_vendor')

def add_hotel(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties= request.POST.getlist('ameneties')
        hotel_price= request.POST.get('hotel_price')
        hotel_offer_price= request.POST.get('hotel_offer_price')
        hotel_location= request.POST.get('hotel_location')
        hotel_slug = generate_slug(hotel_name)

        hotel_vendor = HotelVendor.objects.get(id = request.user.id)



        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor
        )
        for ameneti in ameneties:
            ameneti = Ameneties.objects.get(id = ameneti)
            hotel_obj.ameneties.add(ameneti)


        messages.success(request, "Hotel Created")
        return redirect('/account/add-hotel/')


    ameneties = Ameneties.objects.all()

    return render(request, 'vendor/add_hotel.html', context = {'ameneties' : ameneties})

# accounts/views.py
#other views 

@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    if request.method == "POST":
        image = request.FILES['image']
        HotelImages.objects.create(
        hotel = hotel_obj,
        image = image
        )
        return HttpResponseRedirect(request.path_info)

    return render(request, 'vendor/upload_image.html', context = {'images': hotel_obj.hotel_images.all()})

@login_required(login_url='login_vendor')
def delete_image(request, id): 
    hotel_image = HotelImages.objects.get(id = id)
    hotel_image.delete()
    messages.success(request, "Hotel Image deleted")
    return redirect('/account/dashboard/')


@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    
    # Check if the current user is the owner of the hotel
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        # Retrieve updated hotel details from the form
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        
        # Update hotel object with new details
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        
        messages.success(request, "Hotel Details Updated")

        return HttpResponseRedirect(request.path_info)

    # Retrieve amenities for rendering in the template
    ameneties = Ameneties.objects.all()
    
    # Render the edit_hotel.html template with hotel and amenities as context
    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'ameneties': ameneties})