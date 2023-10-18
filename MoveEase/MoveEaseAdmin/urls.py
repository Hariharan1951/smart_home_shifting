from django.urls import path
from . import views as admin_views

app_name="moveease_admin" # We can use for easy identification amd also we can use same name in different apps when we using mulitple apps.
# While usig the url jinja tag we use like `{% url 'app_name:name' %}`.

urlpatterns = [
    path("MoveEase/", admin_views.admin_home_func, name="admin_home"),
    path("MoveEase/login/", admin_views.admin_login_func, name="admin_login"),
    path("MoveEase/register", admin_views.admin_registration_func, name="admin_registration"),
    path("MoveEase/userChecking/", admin_views.username_checking_func, name="username_checking"),
    path("MoveEase/logout/", admin_views.logout_func, name="logout"),
    path("MoveEase/rejection/", admin_views.reject_func, name="reject"),
    path("MoveEase/orderHistory/", admin_views.admin_order_history_func, name="admin_order_history"),
    path("MoveEase/adminnProfileInfo/", admin_views.admin_profile_update_func, name="admin_profile_update"),
    path("MoveEase/passwordChange/", admin_views.admin_password_change_func, name="admin_password_change"),
    path("MoveEase/couponCodeEdit/", admin_views.coupon_code_edit_func, name="coupon_code_edit"),
    path("MoveEase/couponCodeChange/", admin_views.coupon_code_validity_func, name="validity_change"),
    path("MoveEase/couponDelete/", admin_views.coupon_code_delete_func, name="coupon_delete"),
    path("MoveEase/reviewCaurosel/", admin_views.positive_word_change_func, name="positive_word_change"),
    path("MoveEase/positiveWordsDelete/", admin_views.positive_word_delete_func, name="positive_word_delete"),
]
