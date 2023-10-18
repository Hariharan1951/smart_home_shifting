from django.urls import path
from . import views as user_views

app_name = "moveease_customer" # We can use for easy identification amd also we can use same name in different apps when we using mulitple apps.
# While usig the url jinja tag we use like `{% url 'app_name:name' %}`.

urlpatterns = [
    path('', user_views.home, name="home"),
    path('customer/login/', user_views.login_func, name="customer_login"),
    path("usernameChecking/", user_views.name_checking, name="username_checking"),
    path('logout/', user_views.logout_func, name="logout"),
    path('customer/registraion/', user_views.customer_registration_func, name="customer_registration"),
    path('customer/itemsSelection/', user_views.items_selection_func, name="items_selection"),
    path('customer/customerItemSelection/', user_views.items_selected_by_customer_func, name="items_selected_by_cus"),
    path('customer/packingSection', user_views.packing_section_func, name="packing_section"),
    path('customer/packingSection2/', user_views.packing_confirmation_func, name="packing_section2"),
    path('customer/bookingConfirm/', user_views.booking_confirmation_func, name="booking_confirmation"),
    path('customer/bookingConfirm2/', user_views.booking_confirmation2_func, name="booking_confirmation2"),
    path('customer/getTime/', user_views.get_time_func, name="getTime"),
    path('customer/paymentPage/', user_views.payment_page_func, name="payment_page"),
    path('customer/mailSending/', user_views.email_func, name="email"),
    path('customer/paymentPage/netbanking/', user_views.netbanking_func, name="net_banking"),
    path('customer/paymentPage/paymentUpdate/', user_views.payment_update_func, name="payment_update"),
    path('customer/paymentPage/upiPayment/', user_views.upi_payment_func, name="upi_payment"),
    path('customer/paymentPage/cardPayment/', user_views.card_payment_func, name="card_payment"),
    path('customer/orderHistory/', user_views.customer_order_history_func, name="customer_order_history"),
    path('customer/cancelOrder/', user_views.cancel_order_func, name="cancel_order"),
    path('customer/profileUpdate/', user_views.cus_profile_func, name="cus_profile"),
    path('customer/reviewRating', user_views.review_rating_func, name="review_rating"),
    path('customer/couponCode/', user_views.coupon_code_func, name="coupon_code"),
    path('customer/couponClear/', user_views.clear_coupon_func, name="clear_coupon"),
    path('customer/passwordUpdate/', user_views.cus_password_update_func, name="password_update"),
    path('passwordReset/', user_views.password_reset_func, name="password_reset"),
    path('passwordReset2/', user_views.password_reset2_func, name="password_reset2"),
]