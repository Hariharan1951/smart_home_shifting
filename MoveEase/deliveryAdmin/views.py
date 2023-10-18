from django.shortcuts import render, redirect                # To load the html pages
from django.contrib.auth import authenticate, login, logout  # For Default authentication
from django.views.decorators.csrf import csrf_exempt         # For using ajax, it acts like csrf_token in html pages
from django.contrib.auth.models import User                  # In-built User
from django.contrib import messages                          # To show error messages
from django.http import JsonResponse                         # For transfer data while using ajax
from customer.forms import *                                 # Importing all the classes in the forms.py for using in the html pages
from customer.models import User
from MoveEaseAdmin.models import OrderReceived  
from redmail import gmail
import datetime as dt
from django.db.models import Q                               # Used for filter `or`` queries
from django.contrib.auth.hashers import check_password       #To decode / decrypt the hashed password
import re

# Company Details
company_info = {"name":"MoveEase",  
                "contact_info": "+91 9876543210",
                "email_id":"moveease@gmail.in",
                }

file_name="C:/Users/sivaguru sivakumar/OneDrive/Desktop/Hari_wisetech/django_projects/MoveEase/log_files/moveease_account_entry_log.txt" # File name for log entry

def entry_log_files(file_name, user_name,user_type, message): # Function for entry logs

    try:
        with open(file_name,"a") as file_obj:
            file_obj.writelines([dt.datetime.now().strftime("%Y/%m/%d(%X)"), " | ", user_name, " - ",user_type, " --> ", message,"\n"])

    except Exception:
            print("Error while writing log files")


# Create your views here.

def home_func(request):

    order_received = OrderReceived.objects.filter(alloted_to=request.user.id, order_taken=0)
    order_taken = OrderReceived.objects.filter(alloted_to=request.user.id, order_taken=1, order_completed=0)
    return render(request, "deliveryAdmin/delivery_home.html", {"order_received":order_received, "current_orders":order_taken})


def login_func(request):

    if request.method == "POST":
        name = request.POST.get("username")
        password1 =request.POST.get("password")
        user = authenticate(request, username=name, password=password1)
        if user is not None:
            user_type_check = User.objects.get(username=name)
            if user_type_check.user_type == "DELIVERY PARTNER":
                login(request, user)
                entry_log_files(file_name,request.user.username,request.user.user_type, "Logged in")  # Function call for log file entry


                return redirect("moveease_dp:home")
            else:
                messages.error(request, "Invalid Credentials")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "deliveryAdmin/delivery_login.html")


def registration_func(request):
    
    register = DeliveryPartnerForm()
    if request.method == "POST":
        register = DeliveryPartnerForm(request.POST)
        if register.is_valid():
            register.save()
            return redirect("moveease_dp:dp_login")
    return render(request, "deliveryAdmin/delivery_registration.html", {"form":register})


@csrf_exempt
def username_checking_func(request):
    
    if request.method =="POST":
        name = request.POST.get("user_name")

        try:
            user = User.objects.get(username=name)
            if user.user_type == "DELIVERY PARTNER":
                return JsonResponse({"status":1})
            else:
                return JsonResponse({"status":0})
        except:
            return JsonResponse({"status":0})
        

def logout_func(request):

    if request.user.is_authenticated:
        entry_log_files(file_name,request.user.username,request.user.user_type, "Logged out")  # Function call for log file entry
        logout(request)
    return redirect("moveease_dp:dp_login")
    

@csrf_exempt
def availability_func(request):

    if request.method == "POST":
        available = User.objects.get(id=request.user.id)
        availability  = int(request.POST.get("availability"))
        if availability == 0:
            available.transit = 1
            available.save()
        else:
            available.transit = 0
            available.save()
        return JsonResponse({"status":1})
    

@csrf_exempt
def request_func(request):

    if request.method == "POST":
        try:
            order_id = int(request.POST.get("order_id"))
            dp_id = int(request.POST.get("dp_id"))
            order_received = OrderReceived.objects.get(id=order_id)
            order_received.alloted_to = dp_id
            order_received.save()
            return JsonResponse({"status":1, "order_id":order_id})
        except:
            return JsonResponse({"status":0})
            

    
#Logic for rejection
@csrf_exempt
def order_reject_func(request):

    if request.method == "POST":
        rej_order_id = int(request.POST.get("rej_order_id"))
        order_reject = OrderReceived.objects.get(id=rej_order_id)
        order_reject.order_taken = 0
        order_reject.alloted_to = 0
        order_reject.status ="ORDERED"
        order_reject.save()

        #Logic for availability after accepting the order 
        dp_id = int(request.POST.get("rej_dp_id"))
        available = User.objects.get(id=dp_id)
        available.transit = 0
        available.save()
        return JsonResponse({"stat":1, "order_id":rej_order_id})
    

# sent email to customer
@csrf_exempt
def order_reject_email_func(request):

    if request.method == "POST":
        
        unique_id = request.POST.get("unique_id", "MOVEEASE-YYYYDDMM-HHSS")
        account_id = int(request.POST.get("acc_id"))
        order_date= request.POST.get("order_date", "YYYY-MM-DD")
        order_id = int(request.POST.get("order_id"))
        order_reject = OrderReceived.objects.get(id=order_id)
        order_reject.order_taken = 0
        order_reject.alloted_to = 0
        order_reject.status ="ORDERED"
        order_reject.save()

        #Logic for availability after accepting the order 
        dp_id = int(request.POST.get("delivery"))
        available = User.objects.get(id=dp_id)
        available.transit = 0
        available.save()
        ##################################################################
        #          Cancel Confirmation Email by Delivery Partner         #
        ##################################################################
        try:
            customer_name = User.objects.get(id=account_id)
            mail_id = customer_name.email
            gmail.username = "hariharant998@gmail.com"  # Notification mail sent to registered mail of customer
            gmail.password = "ucnk enny kwnk kxsb"
            gmail.send(subject = f"Order Cancelled by Delivery Partner - Order #{unique_id}",
                        receivers = [mail_id],
                            ##################### Content for email ########################### 
                            html ="""
                            <h3>Dear <em>{{name}}</em>,</h3>
                            <p>I hope this message finds you well. We are writing to confirm the cancellation of your recent order #{{order_no}},
                            which was placed on {{order_date}} by our delivery partner. We would request you to wait for further process untill our delivery partner is assigned to you and also would like to assist you with the process.</p>
                            <p><strong>Order Number:</strong> {{order_no}}<p>
                            <p><strong>Order Date:</strong> {{order_date}}</p>
                        

                            
                            <p>If you have any further questions or concerns related to this cancellation or any other matter, please don't hesitate to contact 
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
                                "company_contact_no": company_info.get("contact_info"),
                                "company_name": company_info.get("name"),
                                "company_email":company_info.get("email_id"),
                                },)
                

            return JsonResponse({"stat":1, "order_id":order_id})
        except:
            return JsonResponse({"status":0})
    

#Logic for order accept by delivery partner
@csrf_exempt
def accept_func(request):

    if request.method == "POST":

        unique_id = request.POST.get("unique_id", "MOVEEASE-YYYYDDMM-HHSS")
        account_id = int(request.POST.get("acc_id"))
        order_id = int(request.POST.get("order_id"))
        order_accept = OrderReceived.objects.get(id=order_id)
        otp = order_accept.otp
        order_accept.order_taken = 1
        order_accept.status ="ORDER CONFIRMED"
        order_accept.save()
    
        #Logic for availability after accepting the order 
        dp_id = int(request.POST.get("dp_id"))
        available = User.objects.get(id=dp_id)
        available.transit = 1
        available.save()
        ################################################################
        #        Email after accepting order by Delivery Parnter       #
        ################################################################
        try:
            customer_name = User.objects.get(id=account_id)
            mail_id = customer_name.email
            gmail.username = "hariharant998@gmail.com"  # Notification mail sent to registered mail of customer
            gmail.password = "ucnk enny kwnk kxsb"
            gmail.send(subject = f"Order Confirmation - Order #{unique_id}",
                        receivers = [mail_id],
                        ##################### Content for email ########################### 
                        html ="""
                            <h3>Dear <em>{{name}}</em>,</h3>
                            <p>We are pleased to inform you that we have successfully confirmed your order #{{order_no}}. Thank you for choosing {{company_name}} for your service needs.</p>
                            <p> Your Delivery partner is ready to pick your order</p>
                            <p><strong>Delivery Agent Name:</strong> {{dp_name}}<p>
                            <p><strong>Delivery Agent Number:</strong> {{dp_ph_no}}</p>

                            <p>This is the OTP:<strong>{{otp}}</strong> you can tell to your delivery partner once the order is delivered. Please do not share with anyone except delivery partner once the order is completed</p>   

                            <p>If you have any questions or concerns about your order, please do not hesitate to contact our customer support team at {{company_email}} or {{company_contact_no}}. Our dedicated team is here to assist you.</p>

                            <p>Thank you for considering {{company_name}} for your house shifting needs. We look forward to serving you and making your move as seamless as possible.</p>

                            <p>Best regards,</p>
                            <p>Shifting Team</p>
                            <p>{{company_name}}</p>
                            <p>{{company_contact_no}}</p>   """,
                            body_params={
                                "name": customer_name.first_name,
                                "order_no":unique_id,
                                "dp_name":available.first_name,
                                "dp_ph_no":available.phone_number,
                                "otp":otp,
                                "company_contact_no": company_info.get("contact_info"),
                                "company_name": company_info.get("name"),
                                "company_email":company_info.get("email_id"),
                                },)    
                    
            return JsonResponse({"status":1, "order_id":order_id})
        except:
            return JsonResponse({"status":0, "order_id":order_id})
        

# Logic for live status update to customer and admin
@csrf_exempt
def live_status_func(request):

    if request.method == "POST":
        try:
            order_id = int(request.POST.get("order_id"))
            status = request.POST.get("status")
            live_status = OrderReceived.objects.get(id=order_id)
            live_status.status = status
            live_status.save()
            return JsonResponse({"status":1})
        except:
            return JsonResponse({"status":0})


# Logic for order completion 
@csrf_exempt
def order_completed_func(request):

    if request.method == "POST":
        try:
            unique_id = request.POST.get("unique_id", "MOVEEASE-YYYYDDMM-HHSS")
            account_id = int(request.POST.get("acc_id"))
            order_date= request.POST.get("order_date", "YYYY-MM-DD")
            order_id = int(request.POST.get("order_id"))
            dp_id = int(request.POST.get("dp_id"))
            dp_details = User.objects.get(id=dp_id)
            order_complete = OrderReceived.objects.get(id=order_id)
            order_complete.delivery_preson_account_id = dp_id
            order_complete.delivery_person_name = dp_details.first_name
            order_complete.delivery_person_ph_no = dp_details.phone_number
            order_complete.delivery_person_email = dp_details.email
            order_complete.order_completed_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order_complete.status = "COMPLETED"
            order_complete.order_completed = 1 # Denotes order completed
            dp_details.transit = 0
            order_complete.save()
            dp_details.save()
            #########################################################
            #          Email Confirmation of order completed        #
            #########################################################

            customer_name = User.objects.get(id=account_id)
            mail_id = customer_name.email
            gmail.username = "hariharant998@gmail.com"  # Notification mail sent to registered mail of customer
            gmail.password = "ucnk enny kwnk kxsb"
            gmail.send(subject = f"Order Delivered Confirmation - Order #{unique_id}",
                        receivers = [mail_id],
                        ##################### Content for email ########################### 
                        html ="""
                        <h3>Dear <em>{{name}}</em>,</h3>
                        <p>We are pleased to inform you that we have successfully received your order #{{order_no}} placed on {{order_date}}. Thank you for choosing {{company_name}} for your service needs.</p>

                        <h5>Order Details:</h5>
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
                        </div>

                        <p>We have received confirmation that your order was successfully delivered to your specified shipping address.
                        If you have any concerns about the delivery or the condition of your order, please contact us immediately at
                        {{company_email}} or {{company_contact_no}}. Your satisfaction is our top priority, and we are here to assist you in any way we can.</p>

                        <p>We hope you continue to enjoy shopping with {{company_name}}. If you have any questions, need assistance,
                        or wish to place another order in the future, please don't hesitate to reach out to us. We are here to provide 
                        you with exceptional service.</p>

                        <p>Thank you for choosing {{company_name}}. We appreciate your business and look forward to serving you again.</p>

                        <p>Best regards,</p>
                        <p>Shifting Team</p>
                        <p>{{company_name}}</p>
                        <p>{{company_contact_no}}</p>   """,
                        body_params={
                            "name": customer_name.first_name,
                            "order_no":unique_id,
                            "order_date":order_date,
                            "payment_mode":order_complete.payment_mode,
                            "company_contact_no": company_info.get("contact_info"),
                            "company_name": company_info.get("name"),
                            "company_email":company_info.get("email_id"),
                            "total_amount": order_complete.total_amount,
                            "from_add": order_complete.fromAddress,
                            "to_add":order_complete.toAddress,
                            "shift_date":order_complete.shifting_date,
                            "total_kms":order_complete.kms_range,
                            "total_count":order_complete.no_of_items,
                            },)
            return JsonResponse({"status":1,"order_id":order_id})
        except:
            return JsonResponse({"status":0})
        

def dp_order_history_func(request):

    order_history = OrderReceived.objects.filter(order_completed = 1, status="COMPLETED", alloted_to=request.user.id)
    if request.method == "POST":
        if request.POST.get("sort-button") == "Sort By Name":
            order_history = order_history.order_by("customer_name")
        elif request.POST.get("sort-button") == "Sort By Date":
            order_history = order_history.order_by("-shifting_date")
        elif request.POST.get("sort-button") == "Sort By Order Id":
            order_history = order_history.order_by("id")
        else:
            shift_date = request.POST.get("date")
            if  shift_date != "":
                try:
                    order_history = OrderReceived.objects.filter(shifting_date=shift_date)
                except:
                    order_history = {}
    return render(request, "deliveryAdmin/deliveryAdmin_order_history.html", {"ordered_history":order_history})


def dp_profile_update_func(request):

    dp_profile = User.objects.get(id=request.user.id)
    if request.method == "POST":        
        f_name = request.POST.get("f-name")
        l_name = request.POST.get("l-name") 
        email = request.POST.get("email") 
        ph_no = request.POST.get("ph-no") 
        vehicle_type = request.POST.get("vehicle-type") 
        vehicle_no = request.POST.get("vehicle-no") 
        dp_profile.first_name = f_name
        dp_profile.last_name = l_name 
        dp_profile.email = email
        dp_profile.phone_number = ph_no 
        dp_profile.vehicle_type = vehicle_type 
        dp_profile.vehicle_no = vehicle_no.upper()
        dp_profile.save()
        
    return render(request, "deliveryAdmin/delivery_profile_update.html", {"dp_profile":dp_profile})


def dp_password_change_func(request):

    dp_password = get_user_model().objects.get(id=request.user.id)
    if request.method == "POST":
        old_password = request.POST.get("old-password")
        new_password = request.POST.get("password1")
        
        if check_password(old_password, dp_password.password):
            if re.findall("[a-z]", new_password) and re.findall("[A-Z]", new_password) and re.findall("[0-9]", new_password) and re.findall("[\!\@\#\$\%\&\*\?]", new_password):
                dp_password.set_password(new_password)
                dp_password.save()
                messages.success(request, "Password changed successfully")
                return redirect("moveease_dp:logout")
            else:
                messages.error(request, "Password must with a combination of uppercase letters, lowercase letters, numbers, and symbols.")
        else:
            messages.error(request, "Wrong Current Password")
    return render(request, "deliveryAdmin/delivery_password_update.html")
