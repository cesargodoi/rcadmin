from django.urls import path

from . import views

urlpatterns = [
    path("", views.center_home, name="center_home"),
    path("<uuid:pk>/detail/", views.center_detail, name="center_detail"),
    path("create/", views.center_create, name="center_create"),
    path(
        "<uuid:pk>/update_basic/",
        views.center_update_basic,
        name="center_update_basic",
    ),
    path(
        "<uuid:pk>/update_address/",
        views.center_update_address,
        name="center_update_address",
    ),
    path(
        "<uuid:pk>/update_others/",
        views.center_update_others,
        name="center_update_others",
    ),
    path(
        "<uuid:pk>/update_image/",
        views.center_update_image,
        name="center_update_image",
    ),
    path("<uuid:pk>/delete/", views.center_delete, name="center_delete"),
    path("<uuid:pk>/reinsert/", views.center_reinsert, name="center_reinsert"),
]
