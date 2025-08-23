from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HotelUser(User):
  profile_picture = models.ImageField(upload_to = 'profiles/users/')
  phone_number = models.CharField(unique = True, max_length = 12)
  email_token = models.EmailField(null = True, blank = True, unique=True)
  otp = models.CharField( max_length = 10,null = True, blank = True)

class HotelVendor(User):
  profile_pic = models.ImageField(upload_to = 'profiles/vendors')
  phone_number = models.CharField(max_length = 12, unique= True)
  email_token = models.EmailField(max_length=100, null= True, blank = True)
  otp = models.CharField(max_length=100,null= True, blank = True)

class Ameneties(models.Model):
  name = models.CharField(max_length= 1000)
  icon  = models.ImageField(upload_to = 'hotels/icon/')

class Hotel(models.Model):
  hotel_name = models.CharField(max_length=100)
  hotel_description = models.TextField()
  hotel_slug = models.SlugField(max_length=1000,unique= True)
  hotel_owner = models.ForeignKey(HotelVendor,on_delete = models.CASCADE, related_name = 'hotels')
  amenities = models.ManyToManyField(Ameneties)
  hotel_price = models.FloatField(max_length=100)
  offer_price = models.FloatField(max_length = 100)
  hotel_location = models.TextField()
  is_active = models.BooleanField(default= True)

class HotelImages(models.Model):
  hotel = models.ForeignKey(Hotel,on_delete= models.CASCADE, related_name = 'hotelImages')
  image = models.ImageField(upload_to= 'hotels')

class HotelManager(models.Model):
  hotel = models.ForeignKey(Hotel,on_delete = models.CASCADE, related_name = 'hotel_management')
  manager_name = models.CharField(max_length= 100)
  manager_contact = models.CharField(max_length= 100)






