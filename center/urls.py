from django.urls import path

from . import views

urlpatterns = [
    path("", views.center_home, name="center_home"),
    path("<uuid:pk>/detail/", views.center_detail, name="center_detail"),
    path("create/", views.center_create, name="center_create"),
    path("<uuid:pk>/update/", views.center_update, name="center_update"),
    path("<uuid:pk>/delete/", views.center_delete, name="center_delete"),
    path("<uuid:pk>/reinsert/", views.center_reinsert, name="center_reinsert"),
]
