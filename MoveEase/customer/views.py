from django.shortcuts import render, redirect                   # To load the html pages
from django.contrib.auth import authenticate, login, logout     # For Default authentication
from django.views.decorators.csrf import csrf_exempt            # For using ajax, it acts like csrf_token in html pages
from django.contrib.auth.models import User                     # In-built User
from django.contrib import messages                             # To show error messages
from django.http import JsonResponse                            # For transfer data while using ajax
from .forms import *                                            # Importing all the classes in the forms.py for using in the html pages
from .models import User
from MoveEaseAdmin.models import ItemsTable, OrderReceived, CouponCodeTable, CouponCountTable, PositiveWords   # For using the items name in the table/databases
import re
from datetime import datetime as dt
import random                                                   # Importing random function for random number in km
from deliveryAdmin.models import VehicleCapicityTable
from redmail import gmail
from datetime import date as dat
from django.contrib.auth.hashers import check_password          # To decode / decrypt the hashed password
from django.db.models import Q                                  # Used for filter `or`` queries



# Company Details
company_info = {"name":"MoveEase",  
                "contact_info": "+91 9876543210",
                "email_id":"moveease@gmail.in",
                }

customer_info = {}                                              # contains all the details

file_name = "C:/Users/sivaguru sivakumar/OneDrive/Desktop/Hari_wisetech/django_projects/MoveEase/log_files/moveease_account_entry_log.txt" # File name for log entry


def entry_log_files(file_name,user_name,user_type, message):    # Function for entry logs

    try:
        with open(file_name,"a") as file_obj:
            file_obj.writelines([dt.now().strftime("%Y/%m/%d(%X)"), " | ", user_name, " - ",user_type, " --> ", message,"\n"])

    except Exception:
            print("Error while writing log files")


# Create your views here.


def home(request):

    km_range = random.randint(10,50)                            # picking random number for kms
    all_customer_reviews = OrderReceived.objects.filter(Q(status="COMPLETED")|Q(status="REJECTED"), customer_rating__gte=3.0) # customer_rating >= 3.0
    positive_words_table = PositiveWords.objects.all()

    customer_reviews = []
    for i in all_customer_reviews:
        if i.customer_review != None:
            for word in positive_words_table:
                if word.positive_words.casefold() in i.customer_review.split(" "):
                    customer_reviews.append({"customer_rating":i.customer_rating,
                                              "customer_review":i.customer_review,
                                              "customer_name":i.customer_name})
                    break
    
    if request.method == "POST":
        name = request.POST.get("name")
        ph_no = request.POST.get("ph_no")
        address1 = request.POST.get("from_address").upper()
        add1_house_rate = request.POST.get("from_bhk")
        add1_floor = request.POST.get("from_floor")
        address2 = request.POST.get("to_address").upper()
        add2_house_rate = request.POST.get("to_bhk")
        add2_floor = request.POST.get("to_floor")
        date = request.POST.get("date")

        customer_info["name"]= name
        customer_info["ph_no"] = ph_no
        customer_info["address1"] = address1
        customer_info["add1_house_rate"] = int(add1_house_rate)
        customer_info["add1_floor"] = int(add1_floor)
        customer_info["address2"] = address2
        customer_info["add2_house_rate"] = int(add2_house_rate)
        customer_info["add2_floor"] = int(add2_floor)
        customer_info["shifting_date"] = date
        customer_info["kms_range"] = km_range
        return redirect("moveease_customer:items_selection")
    return render(request, "customer/home.html", {"customer_reviews":customer_reviews})


def customer_registration_func(request):

    register = CustomerRegistrationForm()                       # We have to use same variable name for getting error messages
    #register = register.visible_fields()                       # Tried for hidden feilds
    if request.method == "POST":
        register = CustomerRegistrationForm(request.POST)       # We have to use same variable name for getting error messages
        if register.is_valid():
            register.save()
            return redirect("moveease_customer:customer_login")
        """
        else:
            register = register.visible_fields() # Tried for hidden fields
        """
    return render(request, "customer/customer_registration.html", {"form":register}) # We have to use same variable name for getting error messages



def cus_profile_func(request):
    
    customer = User.objects.get(id=request.user.id)
    if request.method == "POST":
        f_name = request.POST.get("f-name")
        l_name = request.POST.get("l-name") 
        email = request.POST.get("email") 
        ph_no = request.POST.get("ph-no") 
        street = request.POST.get("street") 
        city = request.POST.get("city") 
        state = request.POST.get("state") 
        zipcode = request.POST.get("zipcode") 

        customer.first_name = f_name
        customer.last_name = l_name 
        customer.email = email
        customer.phone_number = ph_no 
        customer.street = street 
        customer.city = city 
        customer.state = state
        customer.zip_code = zipcode
        customer.save()
    return render(request, "customer/cus_profile.html",{"customer":customer})


def login_func(request):

    if request.method == "POST":
        name = request.POST.get("username")
        password1 =request.POST.get("password")
        user = authenticate(request, username=name, password=password1)
        if user is not None:
            user_type_check = User.objects.get(username=name)
            if user_type_check.user_type == "CUSTOMER":
                login(request, user)
                entry_log_files(file_name,request.user.username,request.user.user_type, "Logged in")    # Function call for log file entry
                
                if customer_info.get("shifting_date") == None:
                    return redirect("moveease_customer:home")   
                else:
                    return redirect("moveease_customer:booking_confirmation")
            else:
                messages.error(request, "Invalid Credentials")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "customer/customer_login.html")


def logout_func(request):

    if request.user.is_authenticated:
        entry_log_files(file_name,request.user.username,request.user.user_type, "Logged out")           # Function call for log file entry
        logout(request)
    return redirect("moveease_customer:home")


@csrf_exempt
def name_checking(request):                                     # AJAX function for checking username 

    if request.method =="POST":
        
        name = request.POST.get("user_name")

        try:
            user = User.objects.get(username=name)
            if user.user_type == "CUSTOMER":
                return JsonResponse({"status":1})
            else:
                return JsonResponse({"status":0})
        except:
            return JsonResponse({"status":0})
        

def items_selection_func(request):

    items = ItemsTable.objects.all()
    items_count=len(items)
    if request.method == "POST":
        pass
    return render(request,"customer/items_selection.html",{"items": items,
                                                           "items_count": items_count,
                                                           "address1": customer_info.get("address1").title(),
                                                            "address2": customer_info.get("address2").title()})


@csrf_exempt
def items_selected_by_customer_func(request):

    if request.method == "POST":
        items = ItemsTable.objects.all()
        items_count=len(items)
        cus_selected_count = request.POST.get("cus_select_count")
        customer_info["cus_selected_count"] = int(cus_selected_count)
        i = 0
        loop_count = 0
        while loop_count < items_count:
            item_id = f"{i}"
            customer_selected_items = request.POST.get(item_id)
            if customer_selected_items != None:
                customer_info[item_id] = int(customer_selected_items)
                loop_count += 1
                i += 1
            else:
                i += 1

        # Vehicle selection Work and Base price calculation
        # Only km based calculation is done (not calculation based on number of items)
        vehicle_selection_dict = {}
        vehicle_selection = VehicleCapicityTable.objects.all().values().order_by("no_of_items")
        for i in vehicle_selection:
            if customer_info["cus_selected_count"] <= i["no_of_items"]:
                vehicle_selection_dict[i["vehicle_type"]]= i["no_of_items"]
        for i in vehicle_selection_dict.keys():
            vehicle_find = VehicleCapicityTable.objects.get(vehicle_type=i)
            price_per_kms= vehicle_find.price_per_km
            total_vehicle_price = price_per_kms * customer_info["kms_range"]
            base_price = total_vehicle_price + customer_info["add1_house_rate"] + customer_info["add1_floor"] + customer_info["add2_house_rate"] + customer_info["add2_floor"]
            customer_info["vehicle_price"] = int(total_vehicle_price)
            customer_info["base_price"] = int(base_price) # Base price based on first vehicle in the vehicle_selection_dict
            break
        customer_info["selected_vehicles_dict"] = vehicle_selection_dict
        
        # items name and count selected by customer
        items_name_count = []
        item_name = list(ItemsTable.objects.all().values())
        for key, value in customer_info.items():
            if key.isnumeric() and value != 0:
                for i,j in enumerate(item_name):
                    if int(key) == j["id"]:
                        items_name_count.append((j["item_name"], value))    # For store in database purpose
        customer_info["items_name_count"] = items_name_count
        return JsonResponse({"status":1}) 
    

def packing_section_func(request):

    return render(request, "customer/packing_cost.html", {"base_price": customer_info.get("base_price"), "customer_info":customer_info})


@csrf_exempt
def packing_confirmation_func(request):
    
    if request.method == "POST":
        customer_info["total_amount"] = request.POST.get("total_amount")
        customer_info["discounted_amount"] = request.POST.get("total_amount")
        customer_info["booking_amount"] = request.POST.get("booking_amount")
        customer_info["coupon_code"] = "None"
        customer_info["coupon_id"] = "None"
        return JsonResponse({"status":1})
    

def booking_confirmation_func(request):

    if customer_info.get("pickup_time") == None:
        pickup = "08:00"
    else:
        pickup = customer_info.get("pickup_time")

    coupon_list = CouponCodeTable.objects.filter(status=0)
    return render(request, "customer/booking_confirmation.html", {"customer_info": customer_info, "pickup":pickup, "coupon_list":coupon_list})


@csrf_exempt
def booking_confirmation2_func(request):
    
    if request.method  == "POST":
        return JsonResponse({"status":1})
    

@csrf_exempt
def get_time_func(request):
    
    if request.method == "POST":
        pickup_time = request.POST.get("pickup_time")
        customer_info["pickup_time"] = pickup_time
        return JsonResponse({"status":1})


def payment_page_func(request):
    
    if request.user.is_authenticated:
        return render(request, "customer/payment_page.html",{"customer_info":customer_info})
    else:
        return redirect("moveease_customer:customer_login")
    

@csrf_exempt    
def email_func(request):

    if request.method == "POST":
        items_value_list = []
        item_count = 1
        item_name = list(ItemsTable.objects.all().values())

        for key, value in customer_info.items():
            if key.isnumeric() and value != 0:
                for i,j in enumerate(item_name):
                    if int(key) == j["id"]:
                        items_value_list.append((item_count, j["item_name"], value)) # For Table used in the email
                        item_count += 1
                        
        mail_id = request.POST.get("mail_id")
        try:
            gmail.username = "hariharant998@gmail.com"          # Notification mail sent to registered mail of customer
            gmail.password = "ucnk enny kwnk kxsb"
            gmail.send(subject = f"{company_info.get('name')} House Shifting - Quote",
                        receivers = [mail_id],
                        ##################### Content for email ########################### 
                        html ="""
                        <h3>Dear <em>{{name}}</em>,</h3>
                        <p>I hope this message finds you well. We wanted to provide you with a comprehensive summary and quote for your upcoming house shifting project.
                        Our team has carefully reviewed your requirements and here is the detailed breakdown:</p>

                        <div style="margin-top:40px;margin-bottom:10px;padding:10px;border:solid 1px black;">
                            
                            <h4>Order Summary</h4>
                            <hr>
                            <p><em>Amount Quoted</em><span style="float : right;">Rs. {{total_amount}}</span> </p>
                            <p><em>Shifting Date</em><span style="float : right;">{{shift_date}} </span> </p>
                            <p><em>Shifting From</em><span style="float : right;">{{from_add}} </span> </p>
                            <p><em>Shifting To</em><span style="float : right;">{{to_add}}</span> </p>
                            <p><em>Total Kms</em><span style="float : right;">{{total_kms}} km</span> </p>
                            <p><em>No.of items added</em><span style="float : right;">{{total_count}}</span> </p>

                            <table style="border:solid 1px black;margin-left:230px;width:500px">
                                <thead style="text-align:center">
                                    <th>S.No</th>
                                    <th>Item name</th>
                                    <th>Quantity</th>
                                </thead>
                                {% for sno, name, count in items %}
                                <tr style="text-align:center">
                                    <td>{{sno}}</td>
                                    <td>{{name}}</td>
                                    <td>{{count}}</td>
                                </tr>
                                {% endfor %}
                            </table>
                            </center>
                            <style>
                                tr{
                                    background-color: #D6EEEE;
                                }
                            </style>
                        </div>

                        <p>Please review this summary and quote carefully. If you have any questions or would like to make any adjustments,
                        please do not hesitate to contact us at {{company_contact_no}}.
                        We are here to ensure a smooth and stress-free shifting process for you.</p>

                        <p>Thank you for considering {{company_name}} for your house shifting needs. We look forward to serving you and making your move as seamless as possible.</p>

                        <p>Best regards,</p>
                        <p>Finance Team</p>
                        <p>{{company_name}}</p>
                        <p>{{company_contact_no}}</p>   """,
                        body_params={
                            "name": customer_info.get("name", "Customer"),
                            "items": items_value_list,
                            "company_contact_no": "+91 9876543210",
                            "company_name": company_info.get("name"),
                            "total_amount": customer_info.get("total_amount", 0),
                            "from_add": customer_info.get("address1", "From"),
                            "to_add":customer_info.get("address2", "To"),
                            "shift_date":customer_info.get("shifting_date", "YYYY-MM-DD"),
                            "total_kms":customer_info.get("kms_range", 0),
                            "total_count":customer_info.get("cus_selected_count", 0) 
                            },)
            return JsonResponse({"status":1})
        except:
            return JsonResponse({"status":0})


def netbanking_func(request):

    return render(request, "customer/netbanking.html", {"customer_info":customer_info})


@csrf_exempt
def payment_update_func(request):

    if request.method == "POST":
        try:
            payment_mode = request.POST.get("payment_mode")
            customer_info["payment_mode"] = payment_mode 

            ##############################################################################################
            #                          Uploading all the values to the database                          #
            ##############################################################################################
            
            or_params = {}

            or_params["account_id"] = request.user.id
            or_params["customer_name"] = customer_info["name"]
            or_params["ph_no"] = customer_info["ph_no"]
            or_params["fromAddress"] = customer_info["address1"]
            or_params["toAddress"] = customer_info["address2"]
            or_params["shifting_date"] = customer_info["shifting_date"]

            # Logic for timing stored in database
            or_params["pickup_time"] = str(dt.strptime(customer_info["pickup_time"],"%H:%M")-dt.strptime("02:00","%H:%M"))
            
            or_params["kms_range"] = int(customer_info["kms_range"])
            or_params["no_of_items"] = int(customer_info["cus_selected_count"])

            #Logic for adding count of the customer selected values to the database
            for name, count in customer_info.get("items_name_count"):
                if re.match("^[A-Za-z]+[\s][\(][[0-9A-Za-z\_\s]+[\)]$", name):
                    name1= name.replace(" (","_")
                    name2 = name1.replace(" ","_")
                    database_name = name2.rstrip(")")
                    or_params[database_name] = int(count)
                else:
                    database_name = name.replace(" ","_")
                    or_params[database_name] = int(count)

            # Substituting the value of discounted amount to total_amount if discount is applied
            if int(customer_info["total_amount"]) > int(customer_info["discounted_amount"]):
                or_params["total_amount"] = int(customer_info["discounted_amount"])
            else:
                or_params["total_amount"] = int(customer_info["total_amount"])


            or_params["booking_amount"] = int(customer_info["booking_amount"])
            
            # Logic for Vehicles selected for customer added to database
            selected_vehicle_names = ""
            for v_name in customer_info.get("selected_vehicles_dict").keys():
                selected_vehicle_names += v_name + ","
            or_params["selected_vehicles"] = selected_vehicle_names
            
            #ordered date
            order_placed_date = dat.today()
            or_params["order_placed_date"] = order_placed_date

            or_params["payment_mode"] = customer_info["payment_mode"]                             # Uploading payment mode

            #creating unique order id
            date_time = dt.now().strftime("%Y%m%d-%H%S")
            order_unique_id = f"{company_info.get('name').upper()}-{date_time}-{request.user.id}" # COMPANYNAME-YYYYMMDD-HHSS-account_id
            or_params["unique_order_id"] = order_unique_id

            #OTP generation
            or_params["otp"] = str(random.randint(100000,999999))

            OrderConfirmation = OrderReceived(**or_params) # Passed as an arbitrary keyword arguments
            OrderConfirmation.save()

            if customer_info["coupon_code"] != "None":
                if customer_info["add_exist_count"] == 1: # Only increase count to that account
                    coupon_count_update = CouponCodeTable.objects.get(coupon_id=int(customer_info["coupon_id"]), customer_acc_id = request.user.id)
                    updated_count = int(coupon_count_update.count_per_user) + 1
                    coupon_count_update.count_per_user = updated_count
                    print("Only increasing")
                    coupon_count_update.save()

                # Coupon not used by any account(fresh coupon) and  Coupon id not used by particular customer
                if customer_info["fresh_coupon_flag"] == 1:
                    coupon_count_entry = CouponCountTable(coupon_id=int(customer_info["coupon_id"]), customer_acc_id = request.user.id, count_per_user= 1)
                    print("New adding")
                    coupon_count_entry.save()

            # Item list
            items_value_list = []
            item_count = 1
            item_name = list(ItemsTable.objects.all().values())
            for key, value in customer_info.items():
                if key.isnumeric() and value != 0:
                    for i,j in enumerate(item_name):
                        if int(key) == j["id"]:
                            items_value_list.append((item_count, j["item_name"], value))          # For Table used in the email
                            item_count += 1
            ################################################
            #          Email Confirmation of order         #
            ################################################

            mail_id = request.user.email
            gmail.username = "hariharant998@gmail.com"          # Notification mail sent to registered mail of customer
            gmail.password = "ucnk enny kwnk kxsb"
            gmail.send(subject = f"Order Received - #{order_unique_id}",
                        receivers = [mail_id],
                        ##################### Content for email ########################### 
                        html ="""
                        <h3>Dear <em>{{name}}</em>,</h3>
                        <p>We are pleased to inform you that we have successfully received your order #{{order_no}} placed on {{order_date}}. Thank you for choosing {{company_name}} for your service needs.</p>

                        <p><strong>Order Number:</strong> {{order_no}}<p>
                        <p><strong>Order Date:</strong> {{order_date}}</p>
                        <p><strong>Payment Method:</strong> {{payment_mode}}</p>
                        <div style="margin-top:40px;margin-bottom:10px;padding:10px;border:solid 1px black;">
                            
                            <h4>Order Summary</h4>
                            <hr>
                            <p><em>Amount Quoted</em><span style="float : right;">Rs. {{total_amount}}</span> </p>
                            <p><em>Shifting Date</em><span style="float : right;">{{shift_date}} </span> </p>
                            <p><em>Shifting From</em><span style="float : right;">{{from_add}} </span> </p>
                            <p><em>Shifting To</em><span style="float : right;">{{to_add}}</span> </p>
                            <p><em>Total Kms</em><span style="float : right;">{{total_kms}} km</span> </p>
                            <p><em>No.of items added</em><span style="float : right;">{{total_count}}</span> </p>
                            <table style="border:solid 1px black;margin-left:230px;width:500px">
                                <thead style="text-align:center">
                                    <th>S.No</th>
                                    <th>Item name</th>
                                    <th>Quantity</th>
                                </thead>
                                {% for sno, name, count in items %}
                                <tr style="text-align:center">
                                    <td>{{sno}}</td>
                                    <td>{{name}}</td>
                                    <td>{{count}}</td>
                                </tr>
                                {% endfor %}
                            </table>
                            </center>
                            <style>
                                tr{
                                    background-color: #D6EEEE;
                                }
                            </style>
                        </div>

                        <p>If you have any questions or concerns about your order, please do not hesitate to contact our customer support team at {{company_email}} or {{company_contact_no}}. Our dedicated team is here to assist you.</p>

                        <p>Thank you for considering {{company_name}} for your house shifting needs. We look forward to serving you and making your move as seamless as possible.</p>

                        <p>Best regards,</p>
                        <p>Shifting Team</p>
                        <p>{{company_name}}</p>
                        <p>{{company_contact_no}}</p>   """,
                        body_params={
                            "name": customer_info.get("name", "Customer"),
                            "order_no":order_unique_id,
                            "order_date":order_placed_date,
                            "payment_mode":customer_info["payment_mode"],
                            "items": items_value_list,
                            "company_contact_no": company_info.get("contact_info"),
                            "company_name": company_info.get("name"),
                            "company_email":company_info.get("email_id"),
                            "total_amount": customer_info.get("total_amount", 0),
                            "from_add": customer_info.get("address1", "From"),
                            "to_add":customer_info.get("address2", "To"),
                            "shift_date":customer_info.get("shifting_date", "YYYY-MM-DD"),
                            "total_kms":customer_info.get("kms_range", 0),
                            "total_count":customer_info.get("cus_selected_count", 0) 
                            },)
            
            order_unique_id = ""                                # Clearing Unique id
            customer_info.clear()                               # Clearing all the keys and values in the customer_info dictionary after payment done
            return JsonResponse({"status":1})
        except:
            return JsonResponse({"status":0})


def upi_payment_func(request):

    return render(request, "customer/upi_payment.html",{"customer_info":customer_info})


def card_payment_func(request):

    return render(request, "customer/card_payment.html", {"customer_info":customer_info})


def customer_order_history_func(request):

    # Current Orders
    live_customer_order = OrderReceived.objects.filter(account_id=request.user.id, order_completed =0, rejected=0, customer_cancellation=0)
    delivery_agent_details = User.objects.filter(user_type="DELIVERY PARTNER")
    delivery_agent_name = {}
    for i in live_customer_order:
        for name in delivery_agent_details:
            if i.alloted_to == name.id:
                delivery_agent_name[i.id] = [(name.first_name, name.phone_number)]
            elif i.alloted_to == 0:
                delivery_agent_name[i.id] = [("NA", "NA")]

    # Total Orders
    order_history = OrderReceived.objects.filter(account_id = request.user.id)
    if request.method == "POST":
        if request.POST.get("sort-button") == "Sort By Name":
            order_history = order_history.order_by("customer_name")
        elif request.POST.get("sort-button") == "Sort By Date":
            order_history = order_history.order_by("-shifting_date")
        elif request.POST.get("sort-button") == "Sort By Order Id":
            order_history = order_history.order_by("id")
        elif request.POST.get("sort-button") == "Sort By Status":
            order_history = order_history.order_by("status")
        else:
            shift_date = request.POST.get("date")
            if  shift_date != "":
                try:
                    order_history = OrderReceived.objects.filter(shifting_date=shift_date)
                except:
                    order_history = {}
    return render(request, "customer/customer_order_page.html",{"live_order":live_customer_order, "dp_name":delivery_agent_name, "order_history":order_history})


@csrf_exempt
def cancel_order_func(request):

    if request.method == "POST":

        unique_id = request.POST.get("unique_id", "MOVEEASE-YYYYDDMM-HHSS")
        order_status = request.POST.get("status")

        total_amount = int(request.POST.get("total_amount"))
        fine_amount = int(request.POST.get("fine_amount"))
        if order_status == "ORDERED":
            refund_amount = total_amount
            cancel_fee = 0
        else:
            refund_amount = total_amount - fine_amount
            cancel_fee = fine_amount
        account_id = int(request.POST.get("acc_id"))
        order_id = int(request.POST.get("order_id"))
        delivery = int(request.POST.get("delivery"))
        order_date= request.POST.get("order_date", "YYYY-MM-DD")
        cancel_order = OrderReceived.objects.get(account_id = request.user.id, id=order_id)
        cancel_order.alloted_to = 0
        cancel_order.status = "REJECTED"
        cancel_order.order_taken = 0
        cancel_order.customer_cancellation = 1
        cancel_order.refund_status = 1
        cancel_order.order_cancel_time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        cancel_order.save()
        if delivery != 0:
            delivery_partner = User.objects.get(id=delivery)
            delivery_partner.transit = 0
            delivery_partner.save()
        try:

            ##########################################################
            #          Cancel Confirmation Email by customer         #
            ##########################################################

            customer_name = User.objects.get(id=account_id)
            mail_id = customer_name.email
            gmail.username = "hariharant998@gmail.com"          # Notification mail sent to registered mail of customer
            gmail.password = "ucnk enny kwnk kxsb"
            gmail.send(subject = f"Order Cancellation Confirmation - Order #{unique_id}",
                        receivers = [mail_id],
                            ##################### Content for email ########################### 
                            html ="""
                            <h3>Dear <em>{{name}}</em>,</h3>
                            <p>I hope this message finds you well. We are writing to confirm the cancellation of your recent order #{{order_no}},
                            which was placed on {{order_date}}. We understand your decision to cancel and would like to assist you with the process.</p>
                            <p><strong>Order Number:</strong> {{order_no}}<p>
                            <p><strong>Order Date:</strong> {{order_date}}</p>
                            <p><strong>Cancellation Amount:</strong> Rs.{{cancel_fee}}</p>
                            <p><strong>Refund Amount:</strong> Rs.{{refund_amount}}</p>

        
                            <p>Your order has been successfully canceled. Your refund amount will be credited to your bank or wallet within 3-5 buisness days.
                            If you have any further questions or concerns related to this cancellation or any other matter, please don't hesitate to contact 
                            our customer support team at {{company_email}} or {{company_contact_no}}. We are here to assist you.</p>
                            <p>We appreciate your interest in {{company_name}}, and we hope to serve you in the future. If you decide to place another order
                            or have any inquiries, please feel free to reach out to us. We are committed to providing you with the best possible customer experience.
                            Thank you for considering {{company_name}}, and we apologize for any inconvenience this cancellation may have caused. We look forward to the
                            opportunity to serve you again.</p>

                            <p>Best regards,</p>
                            <p>Finance Team</p>
                            <p>{{company_name}}</p>
                            <p>{{company_contact_no}}</p>   """,

                            body_params={
                                "name": customer_name.first_name,
                                "order_no":unique_id,
                                "order_date":order_date,
                                "cancel_fee":cancel_fee,
                                "refund_amount":refund_amount,
                                "company_contact_no": company_info.get("contact_info"),
                                "company_name": company_info.get("name"),
                                "company_email":company_info.get("email_id"),
                                },)
            return JsonResponse({"status":1,"order_id":order_id})
        except:
            return JsonResponse({"status":2,"order_id":order_id})
    else:
        return JsonResponse({"status":0})



@csrf_exempt
def review_rating_func(request):

    if request.method == "POST":
        try:
            order_id = int(request.POST.get("order_id"))
            rating = float(request.POST.get("rating"))
            review = request.POST.get("review")
            review_update = OrderReceived.objects.get(id=order_id)
            review_update.customer_review = review
            review_update.customer_rating = rating
            review_update.save()
            return JsonResponse({"status":1,"order_id":order_id})
        except:
            return JsonResponse({"status":0,"order_id":order_id})
        

@csrf_exempt
def coupon_code_func(request):

    if request.method == "POST":
        try:
            coupon_code = request.POST.get("coupon_code")
            total_amount = float(request.POST.get("total_amount", 0))
            account_id = request.user.id
            coupon_apply = CouponCodeTable.objects.get(name=coupon_code)
            if coupon_apply.status == 0:
                offer_percent = int(coupon_apply.offer_percent)
                min_billing = float(coupon_apply.min_billing_amount)
                max_discount = float(coupon_apply.max_discount_rate)
                valid_per_acc = int(coupon_apply.validity_per_account)
                description = coupon_apply.description
                
                # Flag variables
                coupon_code_flag = 0
                fresh_coupon_flag = 0
                add_exist_count = 0
                
                try:
                    coupon_count_check = CouponCountTable.objects.get(coupon_id = coupon_apply.id)
                    try:
                        coupon_acc_count_check = CouponCountTable.objects.get(coupon_id = coupon_apply.id, customer_acc_id=account_id)
                        if valid_per_acc > coupon_acc_count_check.count_per_user:
                            coupon_code_flag = 1
                        else:
                            coupon_code_flag = 0
                    except:                     # Coupon id not used by particular customer
                        fresh_coupon_flag = 1
                        coupon_code_flag = 1
                except:                         # Coupon not used by any account(fresh coupon)
                    fresh_coupon_flag = 1
                    coupon_code_flag = 1

                # Coupon code calculation
                if coupon_code_flag == 1:       # eligible for coupon code calculation
                    if total_amount >= min_billing:
                        original_offer_discount = int((offer_percent / 100) * total_amount)
                        if original_offer_discount > max_discount:
                            discounted_amount = total_amount - max_discount
                            discount = max_discount
                        else:
                            discounted_amount = total_amount - original_offer_discount
                            discount = original_offer_discount

                        if add_exist_count == 1: # Only increase count to that account
                            coupon_count_update = CouponCodeTable.objects.get(coupon_id=coupon_apply.id, customer_acc_id = account_id)
                            updated_count = int(coupon_count_update.count_per_user) + 1
                            coupon_count_update.count_per_user = updated_count
                            print("=================================================================")
                            print("      Only increasing                                           ")
                            print("=================================================================")
                            customer_info["add_exist_count"] = 1
                            customer_info["fresh_coupon_flag"] = 0
                        # Coupon not used by any account(fresh coupon) and  Coupon id not used by particular customer
                        if fresh_coupon_flag == 1:
                            coupon_count_entry = CouponCountTable(coupon_id=coupon_apply.id , customer_acc_id = account_id, count_per_user= 1)
                            print("++++++++++++++++++++++++++++++++++++++++++++")
                            print("         New  adding   ")
                            print("++++++++++++++++++++++++++++++++++++++++++++")
                            customer_info["add_exist_count"] = 0
                            customer_info["fresh_coupon_flag"] = 1
                        customer_info["coupon_code"] = coupon_code.upper()
                        customer_info["coupon_id"] = coupon_apply.id 
                        customer_info["discounted_amount"] = discounted_amount      # saving the discounted amount to the dictionary
                        return JsonResponse({"status":1, "discounted_total_price":discounted_amount, "discount_amount":discount})
                    else:
                        customer_info["coupon_code"] = "None"
                        customer_info["coupon_id"] = "None" 
                        customer_info["add_exist_count"] = 0
                        customer_info["fresh_coupon_flag"] = 0
                        discounted_amount = total_amount
                        discount = 0
                        customer_info["discounted_amount"] = discounted_amount
                        return JsonResponse({"status":2, "description":description, "discounted_total_price":discounted_amount, "discount_amount":discount})
                else:
                    customer_info["add_exist_count"] = 0
                    customer_info["fresh_coupon_flag"] = 0
                    customer_info["coupon_code"] = "None"
                    customer_info["coupon_id"] = "None" 
                    discounted_amount = total_amount
                    discount = 0
                    customer_info["discounted_amount"] = discounted_amount
                    return JsonResponse({"status":0, "discounted_total_price":discounted_amount, "discount_amount":discount})
            else:
                customer_info["add_exist_count"] = 0
                customer_info["fresh_coupon_flag"] = 0
                customer_info["coupon_code"] = "None"
                customer_info["coupon_id"] = "None" 
                discounted_amount = total_amount
                discount = 0
                customer_info["discounted_amount"] = discounted_amount
                return JsonResponse({"status":3,"discounted_total_price":discounted_amount, "discount_amount":discount}) 
        except:
            customer_info["coupon_code"] = "None"
            customer_info["coupon_id"] = "None" 
            customer_info["add_exist_count"] = 0
            customer_info["fresh_coupon_flag"] = 0
            total_amount = float(customer_info.get("total_amount", 0))
            discounted_amount = total_amount
            discount = 0
            customer_info["discounted_amount"] = discounted_amount
            return JsonResponse({"status":0,"discounted_total_price":discounted_amount, "discount_amount":discount})
        

@csrf_exempt
def clear_coupon_func(request):

    if request.method == "POST":
        total_amount = request.POST.get("total_amount", 0)
        customer_info["discounted_amount"] = total_amount
        customer_info["coupon_code"] = "None"
        customer_info["coupon_id"] = "None" 
        customer_info["add_exist_count"] = 0
        customer_info["fresh_coupon_flag"] = 0
        return JsonResponse({"status":1, "discounted_total_price":total_amount})
    else:
        return JsonResponse({"status":0})


def cus_password_update_func(request):

    customer_password = get_user_model().objects.get(id=request.user.id)
    if request.method == "POST":
        old_password = request.POST.get("old-password")
        new_password = request.POST.get("password1")
        if check_password(old_password, customer_password.password):
            if re.findall("[a-z]", new_password) and re.findall("[A-Z]", new_password) and re.findall("[0-9]", new_password) and re.findall("[\!\@\#\$\%\&\*\?]", new_password):
                customer_password.set_password(new_password)    # to set the new password as a hashed password
                customer_password.save()
                messages.success(request, "Password changed successfully")
                return redirect("moveease_customer:logout")
            else:
                messages.error(request, "Password must with a combination of uppercase letters, lowercase letters, numbers, and symbols.")
        else:
            messages.error(request, "Wrong Current Password")

    return render(request, "customer/customer_password_update.html")

@csrf_exempt
def password_reset_func(request): # Password reset for all user type

    if request.method == "POST":
        name = request.POST.get("name")
        user_type = request.POST.get("user_type")
        try:
            password_reset = get_user_model().objects.get(username=name,user_type=user_type)
            otp = str(random.randint(100000, 999999))
            try:

                ##########################################################
                #          Cancel Confirmation Email by customer         #
                ##########################################################

                customer_name = password_reset.username
                mail_id = password_reset.email
                gmail.username = "hariharant998@gmail.com"          # Notification mail sent to registered mail of customer
                gmail.password = "ucnk enny kwnk kxsb"
                gmail.send(subject = f"{company_info.get('name')} - Password Reset Request with OTP",
                            receivers = [mail_id],
                                ##################### Content for email ########################### 
                                html ="""
                                <h3>Dear <em>{{name}}</em>,</h3>
                                <p>We have received a request to reset the password associated with your account. To ensure the security of your account, we are sending you a one-time password (OTP) to verify your identity.</p>
                                <p><strong>Your OTP is:</strong> {{otp}}<p>
            
                                <p>Please follow these steps to reset your password:</p>

                                <p>1. Enter the OTP code you received in this email.</p>

                                <p>2. You will be directed to a page where you can create a new password. Please choose a strong, unique password to enhance the security of your account.</p>

                                <p>3. After setting your new password, you will receive a confirmation message.</p>

                                <p>If you did not request a password reset or believe this request was made in error, please contact our support team immediately at {{company_email}} or {{company_contact_no}}.</p>

                                <p>Please note that the OTP is valid for only one time. Do not share your OTP with anyone.</p>

                                <p>Thank you for using our services.</p>

                                <p>Best regards,</p>
                                <p>{{company_name}}</p>  """,

                                body_params={
                                    "name": customer_name,
                                    "otp":otp,
                                    "company_contact_no": company_info.get("contact_info"),
                                    "company_name": company_info.get("name"),
                                    "company_email":company_info.get("email_id"),
                                    },)
                return JsonResponse({"status":1,"otp":otp})
            except:
                return JsonResponse({"status":2,"otp":otp})
        except:
            return JsonResponse({"status":0})
        

@csrf_exempt
def password_reset2_func(request): # Password reset for all user type

    if request.method == "POST":
        name = request.POST.get("name")
        customer_password = get_user_model().objects.get(username=name)
        password1 = request.POST.get("password")
        if re.findall("[a-z]", password1) and re.findall("[A-Z]", password1) and re.findall("[0-9]", password1) and re.findall("[\!\@\#\$\%\&\*\?]", password1):
            customer_password.set_password(password1)    # to set the new password as a hashed password
            customer_password.save()
            return JsonResponse({"status":1})
        else:
            return JsonResponse({"status":0})
