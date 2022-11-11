import pytest

from django.urls import reverse


#  frequency_ps_view ##########################################################
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("user", 302),
        ("office", 200),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
        ("presidium", 200),
    ],
)
def test_access__frequency_ps_list__by_user_type(
    create_center,
    create_user,
    activity_factory,
    create_event,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    center = create_center(user=create_user(email="u2@mail.com"))
    activity = activity_factory()
    persons = [
        create_person(center=center, email=_email)
        for _email in ["a@a.com", "b@b.com", "c@c.com", "d@d.com"]
    ]

    event = create_event(center=center, activity=activity)
    event.frequencies.add(*persons)

    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("frequency_ps_list", args=[persons[0].id])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("user", 302),
        ("office", 200),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
        ("presidium", 302),
    ],
)
def test_access__frequency_ps_insert__by_user_type(
    create_center,
    create_user,
    activity_factory,
    create_event,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    center = create_center(user=create_user(email="u2@mail.com"))
    activity = activity_factory()
    persons = [
        create_person(center=center, email=_email)
        for _email in ["a@a.com", "b@b.com", "c@c.com", "d@d.com"]
    ]

    event = create_event(center=center, activity=activity)
    event.frequencies.add(*persons)

    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("frequency_ps_insert", args=[persons[0].id])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("user", 302),
        ("office", 200),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
        ("presidium", 302),
    ],
)
def test_access__frequency_ps_delete__by_user_type(
    create_center,
    create_user,
    activity_factory,
    create_event,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    center = create_center(user=create_user(email="u2@mail.com"))
    activity = activity_factory()
    persons = [
        create_person(center=center, email=_email)
        for _email in ["a@a.com", "b@b.com", "c@c.com", "d@d.com"]
    ]

    event = create_event(center=center, activity=activity)
    event.frequencies.add(*persons)

    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("frequency_ps_delete", args=[persons[0].id, event.id])
    response = client.get(url)
    assert response.status_code == status_code
