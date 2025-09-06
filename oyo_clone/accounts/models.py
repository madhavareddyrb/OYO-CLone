from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HotelUser(User):
  profile_picture = models.ImageField(upload_to = 'profiles/users/')
  phone_number = models.CharField(unique = True, max_length = 12)
  email_token = models.EmailField(null = True, blank = True, unique=True)
  otp = models.CharField( max_length = 10,null = True, blank = True)
  is_verified = models.BooleanField(default = False)
  otp = models.CharField(max_length= 10, null = True, blank = True)

class HotelVendor(User):
  profile_pic = models.ImageField(upload_to = 'profiles/vendors')
  phone_number = models.CharField(max_length = 12, unique= True)
  email_token = models.EmailField(max_length=100, null= True, blank = True)
  otp = models.CharField(max_length=100,null= True, blank = True)
  is_verified = models.BooleanField(default = False)
  business_name = models.CharField(max_length=100,null= True, blank = True,default= 'Hotel Vendor')
  

class Ameneties(models.Model):
  name = models.CharField(max_length= 1000)
  icon  = models.ImageField(upload_to = 'hotels/icon/')

  def __str__(self):
    return self.name

class Hotel(models.Model):
  hotel_name = models.CharField(max_length=100)
  hotel_description = models.TextField()
  hotel_slug = models.SlugField(max_length=1000,unique= True,null=True,blank=True)
  hotel_owner = models.ForeignKey(HotelVendor,on_delete = models.CASCADE, related_name = 'hotels')
  ameneties = models.ManyToManyField(Ameneties,blank=True)
  hotel_price = models.FloatField(max_length=100)
  hotel_offer_price = models.FloatField(max_length = 100)
  hotel_location = models.TextField()
  is_active = models.BooleanField(default= True)

  def save(self, ) -> None:
    from utils import generate_slug

    if not self.pk:
      self.hotel_slug =  generate_slug(self.hotel_name)
    return super().save()
  def save(self, *args, **kwargs):   # ✅ Accepts force_insert, force_update
        # put any custom logic here if needed
        super().save(*args, **kwargs)  # ✅ forwards to Django’s save


class HotelImages(models.Model):
  hotel = models.ForeignKey(Hotel,on_delete= models.CASCADE, related_name = 'hotel_images')
  image = models.ImageField(upload_to= 'hotels')

class HotelManager(models.Model):
  hotel = models.ForeignKey(Hotel,on_delete = models.CASCADE, related_name = 'hotel_management')
  manager_name = models.CharField(max_length= 100)
  manager_contact = models.CharField(max_length= 100)






