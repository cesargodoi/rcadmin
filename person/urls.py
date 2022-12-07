from django.urls import path

from .views import (
    frequency_ps,
    historic,
    invitation,
    membership_ps,
    person,
    tools,
    reports,
)

# person
urlpatterns = [
    path("", person.person_home, name="person_home"),
    path("<uuid:id>/detail/", person.person_detail, name="person_detail"),
    path("create/", person.person_create, name="person_create"),
    path(
        "<uuid:id>/update_profile/",
        person.update_profile,
        name="update_profile",
    ),
    path("<uuid:id>/update_pupil/", person.update_pupil, name="update_pupil"),
    path("<uuid:id>/update_image/", person.update_image, name="update_image"),
    path("<uuid:id>/delete/", person.person_delete, name="person_delete"),
    path(
        "<uuid:id>/reinsert/", person.person_reinsert, name="person_reinsert"
    ),
]

# invitation
urlpatterns += [
    path("invitations/", invitation.invitations, name="invitations"),
    path("invitations/list", invitation.invite_list, name="invite_list"),
    path("invitations/invite", invitation.invite, name="invite_person"),
    path(
        "invitations/<uuid:pk>/remove",
        invitation.remove_invite,
        name="remove_invite",
    ),
    path(
        "invitations/send_invitation/<uuid:new_person>",
        invitation.send_invitation,
        name="send_invitation",
    ),
    path(
        "invitations/resend_invitation/<uuid:pk>",
        invitation.resend_invitation,
        name="resend_invitation",
    ),
    path(
        "invitations/confirm_invitation/<uuid:token>/",
        invitation.confirm_invitation,
        name="confirm_invitation",
    ),
    path(
        "invitations/congratulations/<uuid:pk>/",
        invitation.congratulations,
        name="congratulations",
    ),
    path(
        "invitations/reg_feedback/",
        invitation.reg_feedback,
        name="reg_feedback",
    ),
]

# historic
urlpatterns += [
    path(
        "<uuid:person_id>/historic/",
        historic.person_historic,
        name="person_historic",
    ),
    path(
        "<uuid:person_id>/historic/create/",
        historic.historic_create,
        name="historic_create",
    ),
    path(
        "<uuid:person_id>/historic/<int:pk>/update/",
        historic.historic_update,
        name="historic_update",
    ),
    path(
        "<uuid:person_id>/historic/<int:pk>/delete/",
        historic.historic_delete,
        name="historic_delete",
    ),
]

# frequency_ps
urlpatterns += [
    path(
        "<uuid:person_id>/frequencies/",
        frequency_ps.frequency_ps_list,
        name="frequency_ps_list",
    ),
    path(
        "<uuid:person_id>/frequency_insert/",
        frequency_ps.frequency_ps_insert,
        name="frequency_ps_insert",
    ),
    path(
        "<uuid:person_id>/frequency/<uuid:event_id>/delete/",
        frequency_ps.frequency_ps_delete,
        name="frequency_ps_delete",
    ),
]

# membership_ps
urlpatterns += [
    path(
        "<uuid:person_id>/membership_ps/",
        membership_ps.membership_ps_list,
        name="membership_ps_list",
    ),
    path(
        "<uuid:person_id>/membership_ps/create/",
        membership_ps.membership_ps_create,
        name="membership_ps_create",
    ),
    path(
        "<uuid:person_id>/membership_ps/<int:pk>/update/",
        membership_ps.membership_ps_update,
        name="membership_ps_update",
    ),
    path(
        "<uuid:person_id>/membership_ps/<int:pk>/delete/",
        membership_ps.membership_ps_delete,
        name="membership_ps_delete",
    ),
]

# import from seekers
urlpatterns += [
    path(
        "tools/import-from-seekers",
        tools.import_from_seekers,
        name="import_from_seekers",
    ),
    path(
        "tools/import-from-seekers/<int:id>",
        tools.import_seeker,
        name="import_seeker",
    ),
]


# reports
urlpatterns += [
    path(
        "reports/badge/<uuid:person_id>",
        reports.person_badge,
        name="person_badge",
    ),
    path(
        "reports/installed-per-period/",
        reports.installed_per_period,
        name="installed_per_period",
    ),
    path(
        "reports/occurrences-per-period/",
        reports.occurrences_per_period,
        name="occurrences_per_period",
    ),
]
