from django.db import models
# Create your models here.
import datetime

class ItemsTable(models.Model): # Addded to the admin page for dynamic content in future

    item_name_choice = [("FURNITURES",(("SOFA (SINGLE)","Sofa (Single)"),("SOFA (DOUBLE)","Sofa (Double)"),("SOFA (3 SEATER)","Sofa (3 Seater)"),
                        ("SOFA (4 SEATER)","Sofa (4 Seater)"),("BED (SINGLE)","Bed (Single)"),("BED (DOUBLE)","Bed (Double)"),("COT (FOLDING)","Cot (Folding)"),
                        ("MATTRESS (SINGLE)","Mattress (Single)"),("MATTRESS (DOUBLE)","Mattress (Double)"),("DINING TABLE CHAIRS","Dining Table Chairs"),("OFFICE CHAIRS","Office Chairs"),
                        ("PLASTIC CHAIRS","Plastic Chairs"),("DRESSING TABLE","Dressing Table"),("DINING TABLE","Dining Table"),("COMPUTER TABLE","Computer Table"),
                        )),("APPLIANCES",(("TV","TV"),("AC","AC"),("FAN","Fan"),("FRIDGE","Fridge"),
                        ("WASHING MACHINE","Washing Machine"),("GAS STOVE","Gas Stove"),("MICROWAVE OVEN","Microwave Oven"),("WATER PURIFIER","Water Purifier"))),
                        ("VEHICLES",(("BIKE","Bike"),("SCOOTER","Scooter"),("BICYCLE","Bicycle")))]
    
    item_category_choices = [("FURNITURES","Furnitures"),("APPLIANCES","Appliances"),("VEHICLES", "Vehicles")] 
    
    item_name = models.CharField(choices=item_name_choice, max_length=128)
    item_weight_kg = models.FloatField(default=20)
    item_size_ft = models.FloatField(default=2)
    item_category = models.CharField(choices=item_category_choices, max_length=128,default="APPLIANCES")
    fragility = models.IntegerField(default=0) # 1 denotes Fragility and 0 denotes non-fragility
    

    def __str__(self):
        return self.item_name
    

"""
Items added in the database

SOFA (SINGLE)
SOFA (DOUBLE)
SOFA (3 SEATER)
SOFA (4 SEATER)
BED (SINGLE)
BED (DOUBLE)
COT (FOLDING)
MATTRESS (SINGLE)
MATTRESS (DOUBLE)
DINING TABLE CHAIRS
OFFICE CHAIRS
PLASTIC CHAIRS
DRESSING TABLE 
DINING TABLE 
COMPUTER TABLE 
TV
AC 
FAN 
FRIDGE
WASHING MACHINE
GAS STOVE
MICROWAVE OVEN
WATER PURIFIER
BIKE
SCOOTER
BICYCLE
"""

class CouponCodeTable(models.Model):

    name = models.CharField(max_length=128, unique=True)
    offer_percent = models.FloatField(default=0)
    min_billing_amount = models.FloatField(default=0)
    max_discount_rate = models.FloatField(default=0)
    validity_per_account = models.IntegerField(default=0) # How many times this coupon valuable for single account
    description = models.TextField()
    status = models.IntegerField(default=0) # 1 denotes coupon invalid  
    
    def __str__(self):
        return self.name


class CouponCountTable(models.Model):

    coupon_id = models.IntegerField()
    customer_acc_id = models.IntegerField()
    count_per_user = models.IntegerField(default=0)

 
class OrderReceived(models.Model):

    status_choices = [("ORDERED", "Ordered"), ("ORDER CONFIRMED", "Order Confirmed"),
                       ("READY FOR PICKUP", "Ready For Pickup"),("PICKING UP", "Picking Up"),
                         ("TRANSIT", "Transit"),("COMPLETED","Completed"), ("REJECTED","Rejected")]

    payment_mode_choices = [("NET BANKING", "Net Banking"), ("UPI","Upi"),
                             ("CARD", "Card"), ("COD", "Cash on Delivery") ]
    
    unique_order_id = models.CharField(default="MOVEEASE-YYYYMMDD-account_id", max_length=128)
    account_id = models.IntegerField(null=True)
    order_placed_date = models.DateField(null=True)
    customer_name = models.CharField(max_length=128,null=True)
    ph_no = models.CharField(max_length=128,null=True)
    fromAddress = models.CharField(max_length=128, null=True)
    toAddress = models.CharField(max_length=128,null=True) 
    shifting_date = models.DateField()
    pickup_time = models.TimeField(default=datetime.datetime.now())
    kms_range = models.IntegerField(null=True)
    no_of_items = models.IntegerField(null=True)
    SOFA_SINGLE = models.IntegerField(null=True)
    SOFA_DOUBLE = models.IntegerField(null=True)
    SOFA_3_SEATER = models.IntegerField(null=True)
    SOFA_4_SEATER = models.IntegerField(null=True)
    BED_SINGLE = models.IntegerField(null=True)
    BED_DOUBLE = models.IntegerField(null=True)
    COT_FOLDING = models.IntegerField(null=True)
    MATTRESS_SINGLE = models.IntegerField(null=True)
    MATTRESS_DOUBLE = models.IntegerField(null=True)
    DINING_TABLE_CHAIRS = models.IntegerField(null=True)
    OFFICE_CHAIRS = models.IntegerField(null=True)
    PLASTIC_CHAIRS = models.IntegerField(null=True)
    DRESSING_TABLE = models.IntegerField(null=True)
    DINING_TABLE = models.IntegerField(null=True)
    COMPUTER_TABLE = models.IntegerField(null=True)
    TV = models.IntegerField(null=True)
    AC = models.IntegerField(null=True)
    FAN = models.IntegerField(null=True)
    FRIDGE = models.IntegerField(null=True)
    WASHING_MACHINE = models.IntegerField(null=True)
    GAS_STOVE = models.IntegerField(null=True)
    MICROWAVE_OVEN = models.IntegerField(null=True)
    WATER_PURIFIER = models.IntegerField(null=True)
    BIKE = models.IntegerField(null=True)
    SCOOTER = models.IntegerField(null=True)
    BICYCLE = models.IntegerField(null=True)
    total_amount = models.IntegerField(null=True)
    booking_amount = models.IntegerField(null=True)
    selected_vehicles = models.CharField(max_length=1000)
    delivery_preson_account_id = models.IntegerField(null=True)
    delivery_person_name = models.CharField(max_length=128, null=True)
    delivery_person_ph_no = models.CharField(max_length=128, null=True)
    delivery_person_email = models.EmailField(null=True)
    alloted_to = models.IntegerField(default=0)
    status = models.CharField(choices=status_choices, default="ORDERED", max_length=128)
    order_taken = models.IntegerField(default=0) # 1 denotes order taken by delivery partner 
    order_completed = models.IntegerField(default=0) # 1 denotes order completed
    order_completed_time = models.DateTimeField(null=True)
    rejected =models.IntegerField(default=0)# 1 denotes rejected by admin
    payment_mode = models.CharField(choices=payment_mode_choices, default="COD", max_length=128)
    rejection_description = models.TextField(null=True)
    customer_rating = models.FloatField(null=True)
    customer_review = models.TextField(null=True)
    customer_cancellation = models.IntegerField(default=0) # 1 denotes cancelled by customer 
    refund_status = models.IntegerField(default=0) # 0 denotes not a cancelled order, 1 deontes refund pending status after order is cancelled, 2 denotes refund completed after order cancellation
    order_cancel_time = models.DateTimeField(null=True)
    otp = models.CharField(default="000000", max_length=128) # must be put while order delivered by the delivery agent before order delivery confirmation mail


class PositiveWords(models.Model):

    positive_words = models.CharField(max_length=128, default="GOOD")