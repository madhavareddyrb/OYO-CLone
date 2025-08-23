import uuid
from django.core.mail import send_mail
from django.conf import settings

def generateRandomToken():
  return str(uuid.uuid4())

def sendEmailToken():
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