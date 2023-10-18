from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from MoveEaseAdmin.models import ItemsTable

class CustomerRegistrationForm(UserCreationForm):

    user_type_choices = [("CUSTOMER", "Customer")]
    user_type = forms.ChoiceField(choices =user_type_choices)
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email_regex = RegexValidator(regex=r'^[a-zA-Z0-9\.]+@[a-zA-Z]+\.[a-z]{2,3}$', message="Invalid mail id")
    email = forms.EmailField(validators=[email_regex])
    phone_regex = RegexValidator(regex=r'^[6789][0-9]{9}$', message="Phone number must be entered in the format:'9876543210'. Only 10 digits allowed." ) # RegEx pattern for validation 
    phone_number = forms.CharField(validators=[phone_regex], max_length=128)
    door_no = forms.CharField(max_length=128)
    street = forms.CharField(max_length=128)
    city = forms.CharField(max_length=128)
    state = forms.CharField(max_length=128)
    zip_code_regex = RegexValidator(regex=r'^[6][0-9]{5}$', message="Invalid Postal Address")
    zip_code = forms.CharField(validators=[zip_code_regex], max_length=128)

    class Meta():

        model = get_user_model()
        fields = ["user_type", "username", "first_name", "last_name", "email", "phone_number", "door_no", "street", "city", "state", "zip_code", "password1", "password2"]


class MoveEaseAdminForm(UserCreationForm):

    user_type_choices = [("ADMIN", "Admin")]
    user_type = forms.ChoiceField(choices =user_type_choices)
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email_regex = RegexValidator(regex=r'^[a-zA-Z0-9\.]+@[a-zA-Z]+\.[a-z]{2,3}$', message="Invalid mail id")
    email = forms.EmailField(validators=[email_regex])
    phone_regex = RegexValidator(regex=r'^[6789][0-9]{9}$', message="Phone number must be entered in the format:'9876543210'. Only 10 digits allowed." ) # RegEx pattern for validation 
    phone_number = forms.CharField(validators=[phone_regex], max_length=128)

    class Meta():

        model = get_user_model()
        fields = ["user_type", "username", "first_name", "last_name", "email", "phone_number", "password1", "password2"]

    
class DeliveryPartnerForm(UserCreationForm):

    user_type_choices = [("DELIVERY PARTNER", "Delivery Partner")]
    user_type = forms.ChoiceField(choices =user_type_choices)
    vehicle_type_choices = [("TATA ACE", "Tata Ace"),
                ("TATA 407", "Tata 407"),
                ("PICKUP", "Pickup"),
                ("DOST", "Dost"),
                ("SUPER ACE", "Super Ace"),
                ("8FT", "8FT"),
                ("3 WHEELER", "3 Wheeler"),
                ("3 WHEELER ELECTRIC", "3 Wheeler Electric")]
    
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email_regex = RegexValidator(regex=r'^[a-zA-Z0-9\.]+@[a-zA-Z]+\.[a-z]{2,3}$', message="Invalid mail id")
    email = forms.EmailField(validators=[email_regex])
    phone_regex = RegexValidator(regex=r'^[6789][0-9]{9}$', message="Phone number must be entered in the format:'9876543210'. Only 10 digits allowed." ) # RegEx pattern for validation 
    phone_number = forms.CharField(validators=[phone_regex], max_length=128)
    vehicle_type = forms.CharField(widget=forms.Select(choices=vehicle_type_choices), max_length=128)
    vehicle_number_regex = RegexValidator(regex=r'^[a-zA-Z]{2}[0-9]{2}[a-zA-Z]{0,2}[0-9]{4}$', message="Invalid Vehicle Number")
    vehicle_number = forms.CharField(validators=[vehicle_number_regex], max_length=128)

    class Meta():

        model = get_user_model()
        fields = ["user_type", "username", "first_name", "last_name", "email", "phone_number", "vehicle_type", "vehicle_number", "password1", "password2"]
"""
class ItemselectionForm(forms.Form):

    item_name_choice = [("FURNITURES",(("SOFA (SINGLE)","Sofa (Single)"),("SOFA (DOUBLE)","Sofa (Double)"),("SOFA (3 SEATER)","Sofa (3 Seater)"),
                        ("SOFA (4 SEATER)","Sofa (4 Seater)"),("BED (SINGLE)","Bed (Single)"),("BED (DOUBLE)","Bed (Double)"),("COT (FOLDING)","Cot (Folding)"),
                        ("MATTRESS (SINGLE)","Mattress (Single)"),("MATTRESS (DOUBLE)","Mattress (Double)"),("DINING TABLE CHAIRS","Dining Table Chairs"),("OFFICE CHAIRS","Office Chairs"),
                        ("PLASTIC CHAIRS","Plastic Chairs"),("DRESSING TABLE","Dressing Table"),("DINING TABLE","Dining Table"),("COMPUTER TABLE","Computer Table"),
                        )),("APPLIANCES",(("TV","TV"),("AC","AC"),("FAN","Fan"),("FRIDGE","Fridge"),
                        ("WASHING MACHINE","Washing Machine"),("GAS STOVE","Gas Stove"),("MICROWAVE OVEN","Microwave Oven"),("WATER PURIFIER","Water Purifier"))),
                        ("VEHICLES",(("BIKE","Bike"),("SCOOTER","Scooter"),("BICYCLE","Bicycle")))]
    
    
    item_name = forms.MultipleChoiceField(widget=forms.Select(choices=item_name_choice))

    class Meta():
        model = ItemsTable()
        fields = ["item_name"]
        """