from django.urls import path

from . import views

urlpatterns = [
    path("", views.center_home, name="center_home"),
    path("list", views.center_list, name="center_list"),
    path("<uuid:pk>/detail/", views.center_detail, name="center_detail"),
    path("create/", views.center_create, name="center_create"),
    path(
        "<uuid:pk>/update_info/",
        views.center_update_info,
        name="center_update_info",
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
    path(
        "<uuid:pk>/add_responsible/",
        views.center_add_responsible,
        name="center_add_responsible",
    ),
    path(
        "<int:pk>/del_responsible/",
        views.center_del_responsible,
        name="center_del_responsible",
    ),
]
