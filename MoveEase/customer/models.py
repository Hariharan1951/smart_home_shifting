from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

user_choices = [("CUSTOMER", "Customer"),
                ("ADMIN", "Admin"),
                ("DELIVERY PARTNER", "Delivery Partner")]

vehicle_type_choices = [("TATA ACE", "Tata Ace"),
                ("TATA 407", "Tata 407"),
                ("PICKUP", "Pickup"),
                ("DOST", "Dost"),
                ("SUPER ACE", "Super Ace"),
                ("8FT", "8FT"),
                ("3 WHEELER", "3 Wheeler"),
                ("3 WHEELER ELECTRIC", "3 Wheeler Electric")]

class User(AbstractUser):
    user_type = models.CharField(choices=user_choices, max_length=128)
    phone_number=models.CharField(max_length=128, null=True) 
    email = models.EmailField(null=True)

    # Customer
    door_no = models.CharField(max_length=128, null=True)
    street = models.CharField(max_length=128, null=True)
    city = models.CharField(max_length=128, null=True)
    state = models.CharField(max_length=128, null=True)
    zip_code = models.CharField(max_length=128, null=True)

    #delivery
    vehicle_type = models.CharField(choices=vehicle_type_choices, max_length=128, null=True)
    vehicle_number = models.CharField(max_length=128, null=True)
    transit = models.IntegerField(default=0) # 1 indicates is in transit/in picking or 0 indicates vehicle ready to take order 
    
    def is_customer(self):
        if self.user_type == "CUSTOMER":
            return True
        else:
            return False
        
    def is_admin(self):
        if self.user_type == "ADMIN":
            return True
        else:
            return False
    
    def is_delivery_partner(self):
        if self.user_type == "DELIVERY PARTNER":
            return True
        else:
            return False
        

class CustomerTable(models.Model):
    pass
"""
    customer --> phone number, address
    delivery --> phone number, vehicle number, vehicle type

    #user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=0)

    phone_number=models.CharField(max_length=128, null=True, unique=True) 
    email = models.EmailField(unique=True, null=True)

    # Customer
    door_no = models.CharField(max_length=128, null=True)
    street = models.CharField(max_length=128, null=True)
    city = models.CharField(max_length=128, null=True)
    state = models.CharField(max_length=128, null=True)
    zip_code = models.CharField(max_length=128, null=True)

    #delivery
    vehicle_type = models.CharField(max_length=128, null=True)
    vehicle_number = models.CharField(max_length=128, null=True)
"""


    