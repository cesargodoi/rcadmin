from treasury.views.reports import cash_balance
from django.urls import path
from .views import (
    paytypes,
    payments,
    bankflag,
    form_of_payment,
    order,
    reports,
)

## paytypes
urlpatterns = [
    path("paytypes/", paytypes.paytypes, name="paytypes"),
    path("paytypes/create/", paytypes.paytype_create, name="paytype_create"),
    path(
        "paytypes/<int:pk>/update/",
        paytypes.paytype_update,
        name="paytype_update",
    ),
    path(
        "paytypes/<int:pk>/delete/",
        paytypes.paytype_delete,
        name="paytype_delete",
    ),
]

## payments
urlpatterns += [
    path("payments/", payments.payments, name="payments"),
    path("payment/create/", payments.payment_create, name="payment_create"),
    path(
        "payment/<uuid:pk>/update/",
        payments.payment_update,
        name="payment_update",
    ),
    path(
        "payment/<uuid:pk>/delete/",
        payments.payment_delete,
        name="payment_delete",
    ),
]

## bankflags
urlpatterns += [
    path("bankflags/", bankflag.bankflags, name="bankflags"),
    path(
        "bankflags/create/", bankflag.bankflag_create, name="bankflag_create"
    ),
    path(
        "bankflags/<int:pk>/update/",
        bankflag.bankflag_update,
        name="bankflag_update",
    ),
    path(
        "bankflags/<int:pk>/delete/",
        bankflag.bankflag_delete,
        name="bankflag_delete",
    ),
]

## form_of_payment
urlpatterns += [
    path(
        "forms_of_payments/",
        form_of_payment.forms_of_payments,
        name="forms_of_payments",
    ),
    path(
        "form_of_payment/create/",
        form_of_payment.form_of_payment_create,
        name="form_of_payment_create",
    ),
    path(
        "form_of_payment/<uuid:pk>/update/",
        form_of_payment.form_of_payment_update,
        name="form_of_payment_update",
    ),
    path(
        "form_of_payment/<uuid:pk>/delete/",
        form_of_payment.form_of_payment_delete,
        name="form_of_payment_delete",
    ),
]

## orders
urlpatterns += [
    path("orders/", order.orders, name="orders"),
    path("order/create", order.order_create, name="order_create"),
    path(
        "order/search_person/",
        order.order_search_person,
        name="order_search_person",
    ),
    path(
        "order/add_payment/",
        order.order_add_payment,
        name="order_add_payment",
    ),
    path(
        "order/del_payment/<int:pay_id>/",
        order.order_del_payment,
        name="order_del_payment",
    ),
    path(
        "order/add_payform/",
        order.order_add_payform,
        name="order_add_payform",
    ),
    path(
        "order/del_payform/<int:pay_id>/",
        order.order_del_payform,
        name="order_del_payform",
    ),
    path(
        "order/register/",
        order.order_register,
        name="order_register",
    ),
    path(
        "order/<uuid:id>/update/",
        order.order_update,
        name="order_update",
    ),
    path(
        "order/<uuid:id>/detail/",
        order.order_detail,
        name="order_detail",
    ),
    path(
        "order/<uuid:id>/delete/",
        order.order_delete,
        name="order_delete",
    ),
    path(
        "order/<uuid:id>/update_status/",
        order.order_update_status,
        name="order_update_status",
    ),
]

## reports
urlpatterns += [
    path("", reports.treasury_home, name="treasury_home"),
    path("vue/get_order", reports.vue_get_order, name="vue_get_order"),
    path("reports/cash_balance", reports.cash_balance, name="cash_balance"),
    path(
        "reports/period_payments",
        reports.period_payments,
        name="period_payments",
    ),
    path(
        "reports/payments_by_person",
        reports.payments_by_person,
        name="payments_by_person",
    ),
    path(
        "reports/search_person/",
        reports.reports_search_person,
        name="reports_search_person",
    ),
]