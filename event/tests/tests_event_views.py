import pytest
from django.urls import reverse


#  Activity  ##################################################################
@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "_type",
    [("home"), ("create"), ("update"), ("delete")],
)
def test_unlogged_person_cannot_view_activity_page(
    activity_factory, client, _type
):
    """unlogged person can't access any page of activity app"""
    activity = activity_factory()
    page = f"activity_{_type}"
    if _type in ("update", "delete"):
        url = reverse(page, args=[str(activity.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 302),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__activity_home__by_user_type(
    auto_login_user, user_type, status_code
):
    """only 'admin' or 'superuser' can access activity_home"""
    client, user = auto_login_user(group=user_type)
    url = reverse("activity_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 302),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__activity_create__by_user_type(
    auto_login_user, user_type, status_code
):
    """only 'admin' or 'superuser' can access activity_create"""
    client, user = auto_login_user(group=user_type)
    url = reverse("activity_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 302),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__activity_update__by_user_type(
    center_factory,
    activity_factory,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'admin' and 'superuser' can access person_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    activity = activity_factory()
    url = reverse("activity_update", args=[activity.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 302),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__activity_delete__by_user_type(
    center_factory,
    activity_factory,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'admin' and 'superuser' can access person_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    activity = activity_factory()
    url = reverse("activity_delete", args=[activity.pk])
    response = client.get(url)
    assert response.status_code == status_code


#  Event  ##################################################################
@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 200),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__event_home__by_user_type(
    auto_login_user, user_type, status_code
):
    """only 'admin' or 'superuser' can access event_home"""
    client, user = auto_login_user(group=user_type)
    url = reverse("event_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 200),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__event_detail__by_user_type(
    auto_login_user, create_event, user_type, status_code
):
    """only 'admin' or 'superuser' can access event_detail"""
    client, user = auto_login_user(group=user_type)
    event = create_event()
    url = reverse("event_detail", args=[event.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 200),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__event_create__by_user_type(
    auto_login_user, user_type, status_code
):
    """only 'admin' or 'superuser' can access event_create"""
    client, user = auto_login_user(group=user_type)
    url = reverse("event_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 200),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__event_update__by_user_type(
    auto_login_user, create_event, user_type, status_code
):
    """only 'admin' or 'superuser' can access event_update"""
    client, user = auto_login_user(group=user_type)
    event = create_event()
    url = reverse("event_update", args=[event.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.events
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [
        ("admin", 200),
        ("user", 302),
        ("office", 200),
        ("treasury", 302),
        ("treasury_jr", 302),
        ("publicwork", 302),
        ("publicwork_jr", 302),
    ],
)
def test_access__event_delete__by_user_type(
    auto_login_user, create_event, user_type, status_code
):
    """only 'admin' or 'superuser' can access event_delete"""
    client, user = auto_login_user(group=user_type)
    event = create_event()
    url = reverse("event_delete", args=[event.pk])
    response = client.get(url)
    assert response.status_code == status_code
