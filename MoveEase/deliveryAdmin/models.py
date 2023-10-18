from django.db import models

# Create your models here.
class VehicleCapicityTable(models.Model): # Added to admin page for dyanmic change of content 
    vehicle_type_choices = [("TATA ACE", "Tata Ace"),
                ("TATA 407", "Tata 407"),
                ("PICKUP", "Pickup"),
                ("DOST", "Dost"),
                ("SUPER ACE", "Super Ace"),
                ("8FT", "8FT"),
                ("3 WHEELER", "3 Wheeler"),
                ("3 WHEELER ELECTRIC", "3 Wheeler Electric")]
    vehicle_type = models.CharField(choices=vehicle_type_choices, max_length=128)
    vehicle_load_capacity_kg = models.FloatField(default=500) 
    vehicle_length_feet = models.FloatField(default=3.5) 
    price_per_km = models.FloatField(default=50)
    no_of_items = models.IntegerField(default=10)
    
    def __str__(self):
        return self.vehicle_type
