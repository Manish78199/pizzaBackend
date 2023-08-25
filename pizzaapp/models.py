from django.db import models
from django.utils import timezone
# Create your models here.
class Product(models.Model): 
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    product_category=models.CharField(max_length=100,default="")
    
    product_details=models.CharField(max_length=200 ,default="")
    product_price=models.IntegerField()
    product_image=models.ImageField(upload_to="media/",default="")
    product_publish_date=models.DateField(default=timezone.now)
    def __str__(self) :
        return "#"+str(self.id)+" ("+self.product_name+")"
    
class User(models.Model):
    user_name=models.CharField(max_length=30 ,default="")
    user_email=models.CharField(max_length=50 ,default="",unique=True)
    user_password=models.CharField(max_length=20,default="")
    def __str__(self) :
        return self.user_name
    
class Vendor(models.Model):
    user_name=models.CharField(max_length=30 ,default="")
    user_email=models.CharField(max_length=50 ,default="",unique=True)
    user_password=models.CharField(max_length=20,default="")
    def __str__(self) :
        return self.user_name
    
# class Admin(models.Model):
#     user_name=models.CharField(max_length=30 ,default="")
#     user_email=models.CharField(max_length=50 ,default="")
#     user_password=models.CharField(max_length=20,default="")
#     def __str__(self) :
#         return self.user_name
    
class Cart(models.Model):    
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    items=models.CharField(max_length=1000,default="")
    