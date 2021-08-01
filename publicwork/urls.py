from django.urls import path

# from django.contrib.auth import views

from .views import (
    seeker,
    lecture,
    listener,
    report,
    historic,
    group,
    insert_yourself,
)

# publicwork
urlpatterns = [
    path("", report.publicwork_home, name="publicwork_home"),
]

# insert yourself as a member
urlpatterns += [
    path(
        "i-want-to-be-a-member/",
        insert_yourself.insert_yourself,
        name="insert_yourself",
    ),
    path(
        "i-want-to-be-a-member/feedback/",
        insert_yourself.feedback,
        name="feedback",
    ),
    path(
        "i-want-to-be-a-member/confirm-email/<uuid:token>/",
        insert_yourself.confirm_email,
        name="confirm_email",
    ),
]

# seeker
urlpatterns += [
    path("seeker/", seeker.seeker_home, name="seeker_home"),
    path(
        "seeker/<int:pk>/detail/", seeker.seeker_detail, name="seeker_detail"
    ),
    path("seeker/create/", seeker.seeker_create, name="seeker_create"),
    path(
        "seeker/<int:pk>/update/", seeker.seeker_update, name="seeker_update"
    ),
    path(
        "seeker/<int:pk>/delete/", seeker.seeker_delete, name="seeker_delete"
    ),
    path(
        "seeker/<int:pk>/reinsert/",
        seeker.seeker_reinsert,
        name="seeker_reinsert",
    ),
    path(
        "seeker/<int:pk>/frequencies/",
        seeker.seeker_frequencies,
        name="seeker_frequencies",
    ),
    path(
        "seeker/<int:pk>/historic/",
        seeker.seeker_historic,
        name="seeker_historic",
    ),
]

# lecture
urlpatterns += [
    path("lecture/", lecture.lecture_home, name="lecture_home"),
    path(
        "lecture/<int:pk>/detail/",
        lecture.lecture_detail,
        name="lecture_detail",
    ),
    path("lecture/create/", lecture.lecture_create, name="lecture_create"),
    path(
        "lecture/<int:pk>/update/",
        lecture.lecture_update,
        name="lecture_update",
    ),
    path(
        "lecture/<int:pk>/delete/",
        lecture.lecture_delete,
        name="lecture_delete",
    ),
]

# listener
urlpatterns += [
    path(
        "lecture/<int:lect_pk>/add-listener/",
        listener.add_listener,
        name="add_listener",
    ),
    path(
        "lecture/<int:lect_pk>/update-listener/<int:lstn_pk>/",
        listener.update_listener,
        name="update_listener",
    ),
    path(
        "lecture/<int:lect_pk>/remove-listener/<int:lstn_pk>/",
        listener.remove_listener,
        name="remove_listener",
    ),
    path(
        "seeker/<int:pk>/add-frequency/",
        listener.add_frequency,
        name="add_frequency",
    ),
    path(
        "seeker/<int:seek_pk>/update-frequency/<int:freq_pk>/",
        listener.update_frequency,
        name="update_frequency",
    ),
    path(
        "seeker/<int:seek_pk>/remove-frequency/<int:freq_pk>/",
        listener.remove_frequency,
        name="remove_frequency",
    ),
]

# historics
urlpatterns += [
    path(
        "seeker/<int:pk>/create-historic/",
        historic.create_historic,
        name="create_historic",
    ),
    path(
        "seeker/<int:seek_pk>/update-historic/<int:hist_pk>/",
        historic.update_historic,
        name="update_historic",
    ),
    path(
        "seeker/<int:seek_pk>/delete-historic/<int:hist_pk>/",
        historic.delete_historic,
        name="delete_historic",
    ),
]

# groups
urlpatterns += [
    path("group/", group.group_home, name="group_home"),
    path("group/<int:pk>/detail/", group.group_detail, name="group_detail"),
    path("group/create/", group.group_create, name="group_create"),
    path("group/<int:pk>/update/", group.group_update, name="group_update"),
    path("group/<int:pk>/delete/", group.group_delete, name="group_delete"),
    path(
        "group/<int:pk>/reinsert/",
        group.group_reinsert,
        name="group_reinsert",
    ),
    path(
        "group/<int:pk>/frequencies/",
        group.group_frequencies,
        name="group_frequencies",
    ),
    path(
        "group/<int:pk>/frequencies/add/",
        group.group_add_frequencies,
        name="group_add_frequencies",
    ),
    path(
        "group/<int:pk>/member/add/",
        group.group_add_member,
        name="group_add_member",
    ),
    path(
        "group/<int:group_pk>/member/<int:member_pk>/remove/",
        group.group_remove_member,
        name="group_remove_member",
    ),
    path(
        "group/<int:pk>/mentor/add/",
        group.group_add_mentor,
        name="group_add_mentor",
    ),
    path(
        "group/<int:group_pk>/mentor/<uuid:mentor_pk>/remove/",
        group.group_remove_mentor,
        name="group_remove_mentor",
    ),
]

# reports
urlpatterns += [
    path(
        "report/frequencies-per-period/",
        report.frequencies_per_period,
        name="frequencies_per_period",
    ),
    path(
        "report/lectures-per-period/",
        report.lectures_per_period,
        name="lectures_per_period",
    ),
    path(
        "report/status-per-center/",
        report.status_per_center,
        name="status_per_center",
    ),
]
