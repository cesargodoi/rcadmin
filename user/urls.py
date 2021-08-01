from django.urls import path
from django.contrib.auth import views
from . import views as user_views


# user
urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(template_name="user/auth/login.html"),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(template_name="user/auth/logout.html"),
        name="logout",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="user/auth/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="user/auth/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="user/auth/password_reset_form.html",
            email_template_name="user/auth/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done",
        views.PasswordResetDoneView.as_view(
            template_name="user/auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="user/auth/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done",
        views.PasswordResetCompleteView.as_view(
            template_name="user/auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

# profile
urlpatterns += [
    path("profile/detail/", user_views.profile_detail, name="profile_detail"),
    path("profile/update/", user_views.profile_update, name="profile_update"),
    path(
        "profile/historic/",
        user_views.user_historic,
        name="user_historic",
    ),
    path(
        "profile/frequencies/",
        user_views.user_frequencies,
        name="user_frequencies",
    ),
    path(
        "profile/frequencies/scan_qrcode_event/",
        user_views.scan_qrcode_event,
        name="scan_qrcode_event",
    ),
    path(
        "profile/payments/",
        user_views.user_payments,
        name="user_payments",
    ),
    path(
        "profile/new_order/",
        user_views.user_new_order,
        name="user_new_order",
    ),
    path(
        "profile/add_payment/",
        user_views.add_payment,
        name="user_add_payment",
    ),
    path(
        "profile/del_payment/<int:pay_id>/",
        user_views.del_payment,
        name="user_del_payment",
    ),
]
