from django.shortcuts import render, redirect                # To load the html pages
from django.contrib.auth import authenticate, login, logout  # For Default authentication
from django.views.decorators.csrf import csrf_exempt         # For using ajax, it acts like csrf_token in html pages
from django.contrib.auth.models import User                  # In-built User
from django.contrib import messages                          # To show error messages
from django.http import JsonResponse                         # For transfer data while using ajax
from customer.forms import *                                 # Importing all the classes in the forms.py for using in the html pages
from .forms import CouponCodeTaleForm
from customer.models import User
from deliveryAdmin.models import VehicleCapicityTable
from .models import OrderReceived, CouponCodeTable, PositiveWords,ItemsTable
from redmail import gmail
from django.db.models import Q                               # Used for filter `or`` queries
import re
from django.contrib.auth.hashers import check_password       # To decode / decrypt the hashed password
import datetime as dt 



# Create your views here.

# Company Details
company_info = {"name":"MoveEase",  
                "contact_info": "+91 9876543210",
                "email_id":"moveease@gmail.in",
                }

file_name = "C:/Users/sivaguru sivakumar/OneDrive/Desktop/Hari_wisetech/django_projects/MoveEase/log_files/moveease_account_entry_log.txt" # File name for log entry

def entry_log_files(file_name,user_name,user_type, message): # Function for entry logs

    try:
        with open(file_name,"a") as file_obj:
            file_obj.writelines([dt.datetime.now().strftime("%Y/%m/%d(%X)"), " | ", user_name, " - ",user_type, " --> ", message,"\n"])

    except Exception:
            print("Error while writing log files")


def admin_home_func(request):
    
    try:
        vehicle_capacity = VehicleCapicityTable.objects.all().order_by("no_of_items")
        order_received = OrderReceived.objects.filter(order_taken=0, alloted_to=0, rejected=0, customer_cancellation = 0).order_by("shifting_date", "pickup_time")
        avail_delivery_agents = User.objects.filter(transit=0, user_type="DELIVERY PARTNER")
        vehicle_for_customer={}

        # Logic for select button in allotment
        for i in order_received:
            for vehicle in vehicle_capacity:
                for available in avail_delivery_agents:
                    if (vehicle.vehicle_type in i.selected_vehicles.split(","))  and (vehicle.vehicle_type == available.vehicle_type):
                        if vehicle_for_customer.get(i.id) == None:
                            vehicle_for_customer[i.id] = []
                            vehicle_for_customer[i.id].append((available.id, available.first_name))
                        else:
                            vehicle_for_customer[i.id].append((available.id, available.first_name))
    except:
        order_received = {}

    try:
        order_transit = OrderReceived.objects.filter(order_completed=0, order_taken=1)
        delivery_agent = {}
        delivery_agent_name = User.objects.filter(user_type="DELIVERY PARTNER")
        for i in order_transit:
            for k in delivery_agent_name:
                if i.alloted_to == k.id:
                    delivery_agent[i.id]=k.first_name
    except:
        order_transit={}
    
    return render(request, "MoveEaseAdmin/admin_home.html", {"order_received":order_received, "order_transit":order_transit, "vehicle_for_customer":vehicle_for_customer, "delivery_agent_name":delivery_agent})


def admin_login_func(request):

    if request.method == "POST":
        name = request.POST.get("username")
        password1 =request.POST.get("password")
        user = authenticate(request, username=name, password=password1)
        if user is not None:
            user_type_check = User.objects.get(username=name)
            if user_type_check.user_type == "ADMIN":
                login(request, user)
                entry_log_files(file_name,request.user.username,request.user.user_type, "Logged in")  # Function call for log file entry
                print(request.user.user_type)
                return redirect("moveease_admin:admin_home")
            else:
                messages.error(request, "Invalid Credentials")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "MoveEaseAdmin/admin_login.html")


def admin_registration_func(request):
    
    register = MoveEaseAdminForm()
    if request.method == "POST":
        register = MoveEaseAdminForm(request.POST)
        if register.is_valid():
            register.save()
            return redirect("moveease_admin:admin_login")
    return render(request, "MoveEaseAdmin/admin_registration.html", {"form":register})


@csrf_exempt
def username_checking_func(request):

    if request.method =="POST":
        name = request.POST.get("user_name")
        try:
            user = User.objects.get(username=name)
            if user.user_type == "ADMIN":
                return JsonResponse({"status":1})
            else:
                return JsonResponse({"status":0})
        except:
            return JsonResponse({"status":0})
        

def logout_func(request):

    if request.user.is_authenticated:
        entry_log_files(file_name, request.user.username,request.user.user_type, "Logged out")  # Function call for log file entry
        logout(request)
    return redirect("moveease_admin:admin_login")


@csrf_exempt
def reject_func(request):

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
        order_date= request.POST.get("order_date", "YYYY-MM-DD")
        order_id = int(request.POST.get("order_id"))
        order_rejection = OrderReceived.objects.get(id=order_id)
        order_rejection.status = "REJECTED"
        order_rejection.rejected = 1
        order_rejection.save()
        try:
            ##########################################################
            #          Cancel Confirmation(admin) Email              #
            ##########################################################

            customer_name = User.objects.get(id=account_id)
            mail_id = customer_name.email
            gmail.username = "hariharant998@gmail.com"  # Notification mail sent to registered mail of customer
            gmail.password = "ucnk enny kwnk kxsb"
            gmail.send(subject = f"Order Cancellation Confirmation - Order #{unique_id}",
                        receivers = [mail_id],
                            ##################### Content for email ########################### 
                            html ="""
                            <h3>Dear <em>{{name}}</em>,</h3>
                            <p>I hope this message finds you well. We are writing to confirm the cancellation of your recent order #{{order_no}},
                            which was placed on {{order_date}}. Sorry! {{name}}, Our team has decided to cancel your order due to inconvenience and would like to assist you with the process.</p>
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
            return JsonResponse({"status":1, "order_id":order_id})
        except:
            return JsonResponse({"status":0, "order_id":order_id})


def admin_order_history_func(request):
    
    order_history = OrderReceived.objects.filter(Q(status="COMPLETED") | Q(status="REJECTED"))
    if request.method == "POST":
        if request.POST.get("sort-button") == "Sort By Name":
            order_history = order_history.order_by("customer_name")
        elif request.POST.get("sort-button") == "Sort By Date":
            order_history = order_history.order_by("-shifting_date")
        elif request.POST.get("sort-button") == "Sort By Status":
            order_history = order_history.order_by("status")
        elif request.POST.get("sort-button") == "Sort By Order Id":
            order_history = order_history.order_by("id")
        elif request.POST.get("sort-button") == "Sort By Delivery":
            order_history = order_history.order_by("-delivery_person_name")
        else:
            order_id = request.POST.get("order-id")
            if  order_id != "":
                try:
                    order_history = OrderReceived.objects.filter(Q(status="COMPLETED") | Q(status="REJECTED"),id=int(order_id))
                except:
                    order_history = {}
    return render(request, "MoveEaseAdmin/delivery_order_history.html", {"order_history":order_history})


def admin_profile_update_func(request):
    
    admin = User.objects.get(id=request.user.id)
    if request.method == "POST":
        f_name = request.POST.get("f-name")
        l_name = request.POST.get("l-name") 
        email = request.POST.get("email") 
        ph_no = request.POST.get("ph-no") 
        admin.first_name = f_name
        admin.last_name = l_name 
        admin.email = email
        admin.phone_number = ph_no 
        admin.save()
    return render(request, "MoveEaseAdmin/admin_profile_update.html",{"customer":admin})


def admin_password_change_func(request):

    admin_password = get_user_model().objects.get(id=request.user.id)
    if request.method == "POST":
        old_password = request.POST.get("old-password")
        new_password = request.POST.get("password1")
        if check_password(old_password, admin_password.password):
            if re.findall("[a-z]", new_password) and re.findall("[A-Z]", new_password) and re.findall("[0-9]", new_password) and re.findall("[\!\@\#\$\%\&\*\?]", new_password):
                admin_password.set_password(new_password)
                admin_password.save()
                messages.success(request, "Password changed successfully")
                return redirect("moveease_admin:logout")
            else:
                messages.error(request, "Password must with a combination of uppercase letters, lowercase letters, numbers, and symbols.")
        else:
            messages.error(request, "Wrong Current Password")
    return render(request, "MoveEaseAdmin/admin_password_update.html")


def coupon_code_edit_func(request):

    coupon_code = CouponCodeTable.objects.all()
    if request.method == "POST":
        name = request.POST.get("name").upper()
        offer_percent = int(request.POST.get("off-per"))
        bill_amount = int(request.POST.get("min-bill-amt"))
        max_rate = int(request.POST.get("max-dis-amt"))
        validity = int(request.POST.get("validity"))
        description = request.POST.get("description").capitalize()
        try:
            coupon_add = CouponCodeTable.objects.get(name=name)
            coupon_add.offer_percent = offer_percent
            coupon_add.min_billing_amount = bill_amount
            coupon_add.max_discount_rate = max_rate
            coupon_add.validity_per_account = validity
            coupon_add.description = description
            coupon_add.save()
            messages.success(request, "Updated successfully!!")    
        except:
            coupon_add = CouponCodeTable(name=name, offer_percent= offer_percent,min_billing_amount = bill_amount,
                                         max_discount_rate = max_rate, validity_per_account=validity, description=description)
            coupon_add.save()
            messages.success(request, "Added Successfully!!")
    return render(request, "MoveEaseAdmin/coupon_code_edit.html", {"coupon_code":coupon_code,})


@csrf_exempt
def coupon_code_validity_func(request):

    if request.method == "POST":
        try:
            code_id = int(request.POST.get("code_id"))
            validity = int(request.POST.get("validity"))
            code_status_change = CouponCodeTable.objects.get(id=code_id)
            if validity == 0:
                code_status_change.status = 1
                code_status_change.save()
            else:
                code_status_change.status = 0
                code_status_change.save()
            return JsonResponse({"status":1})
        except:
            return JsonResponse({"status":0})
        


@csrf_exempt 
def coupon_code_delete_func(request):

    if request.method == "POST":
        try:
            code_id = int(request.POST.get("code_id"))
            code_delete = CouponCodeTable.objects.get(id=code_id)
            code_delete.delete()
            return JsonResponse({"status":1, "code_id":code_id})
        except:
            return JsonResponse({"status":0})
        

def positive_word_change_func(request):

    positive_word = PositiveWords.objects.all()
    if request.method == "POST":
        name = request.POST.get("name").upper()
        try:
            positive_word_add = PositiveWords.objects.get(positive_words=name)
            positive_word_add.positive_words = name
            positive_word_add.save()
            messages.success(request, "Updated successfully!!")      
        except:
            positive_word_add = PositiveWords(positive_words=name)
            positive_word_add.save()
            messages.success(request, "Added Successfully!!")
    return render(request, "MoveEaseAdmin/review_carousel.html", {"positive_word":positive_word,})


@csrf_exempt 
def positive_word_delete_func(request):

    if request.method == "POST":
        try:
            code_id = int(request.POST.get("code_id"))
            code_delete = PositiveWords.objects.get(id=code_id)
            code_delete.delete()
            return JsonResponse({"status":1, "code_id":code_id})
        except:
            return JsonResponse({"status":0})