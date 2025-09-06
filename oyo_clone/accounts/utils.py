import uuid
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from django.utils.text import slugify
from .views import *



def generateRandomToken():
  return str(uuid.uuid4())

def sendEmailToken(email,token):
  subject = "Please veriry Your email address"
  message = f""" Hi Please verity your email address by clicking below link hhtp://127.0.0.1:8000/account/verify-account/{token}

"""
  send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently = False,
  )

def sendOTPtoEmail(email, otp):
  subject = 'OTP for Login to Your account'
  message = f"""Hello {email}, use these OTP to login {otp}"""
  send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently = False,
  )



def generate_slug(hotel_name):
  slug = slugify(hotel_name) +"-"+ str((uuid.uuid4())).split('-')[0]
  if Hotel.objects.filter(hotel_slug =  slug).exists():
    return generate_slug(hotel_name)
  return slug
