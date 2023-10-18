from django.urls import path
from deliveryAdmin import views as delivery_views

app_name = "moveease_dp" # dp --> delivery partner
urlpatterns = [
    path("delivery/home/", delivery_views.home_func, name="home"),
    path("delivery/login/", delivery_views.login_func, name="dp_login"),
    path("delivery/register/", delivery_views.registration_func, name="dp_registration"),
    path("delivery/nameCheckin/", delivery_views.username_checking_func, name="username_checking"),
    path("delivery/logout/", delivery_views.logout_func, name="logout"),
    path("delivery/availability/", delivery_views.availability_func, name="availability"),
    path("delivery/acceptingRequest/", delivery_views.request_func, name="request_order"),
    path("delivery/acceptOrder/", delivery_views.accept_func, name="accept_order"),
    path("delivery/rejectOrder/", delivery_views.order_reject_func, name="reject_order"),
    path("delivery/rejectOrder1/", delivery_views.order_reject_email_func, name="reject_order_email"),
    path("delivery/liveStatus/", delivery_views.live_status_func, name="live_status"),
    path("delivery/orderCompletion/", delivery_views.order_completed_func, name="order_completed"),
    path("delivery/orderHistory/", delivery_views.dp_order_history_func, name="dp_order_history"),
    path("delivery/profileUpdate/", delivery_views.dp_profile_update_func, name="dp_profile_update"),
    path("delivery/passwordUpdate/",delivery_views.dp_password_change_func, name="dp_password_change"),
]
