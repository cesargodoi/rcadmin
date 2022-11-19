import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


@pytest.mark.django_db
@pytest.mark.parametrize(
    "_type",
    [("add"), ("update"), ("remove")],
)
def test_unlogged_user_cannot_add_update_delete_listener(
    center_factory, create_lecture, create_seeker, client, _type
):
    """
    unlogged user can't access
    'add_listener', 'update_listener', 'remove_listener'
    """
    center = center_factory.create()
    lecture = create_lecture(center=center)
    seeker = create_seeker(center=center)
    page = f"{_type}_listener"
    if _type == "add":
        url = reverse(page, args=[str(lecture.pk)])
    else:
        url = reverse(page, args=[str(lecture.pk), str(seeker.pk)])
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "_type",
    [("add"), ("update"), ("remove")],
)
def test_unlogged_user_cannot_add_update_delete_frequency(
    center_factory, create_lecture, create_seeker, client, _type
):
    """
    unlogged user can't access
    'add_frequency', 'update_frequency', 'remove_frequency'
    """
    center = center_factory.create()
    lecture = create_lecture(center=center)
    seeker = create_seeker(center=center)
    page = f"{_type}_frequency"
    if _type == "add":
        url = reverse(page, args=[str(lecture.pk)])
    else:
        url = reverse(page, args=[str(lecture.pk), str(seeker.pk)])
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__add_listener__by_user_type(
    center_factory, create_lecture, auto_login_user, user_type, status_code
):
    """only 'publicwork' and 'publicwork_jr' can access add_listener"""
    center = center_factory.create()
    lecture = create_lecture(center=center)
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("add_listener", args=[lecture.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__update_listener__by_user_type(
    center_factory,
    create_lecture,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access update_listener"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    lecture = create_lecture(center=center)
    lecture.listeners.add(seeker)
    listener = lecture.listeners.first()
    url = reverse("update_listener", args=[lecture.pk, listener.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__remove_listener__by_user_type(
    center_factory,
    create_lecture,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access remove_listener"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    lecture = create_lecture(center=center)
    lecture.listeners.add(seeker)
    listener = lecture.listeners.first()
    url = reverse("remove_listener", args=[lecture.pk, listener.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__add_frequency__by_user_type(
    center_factory, create_seeker, auto_login_user, user_type, status_code
):
    """only 'publicwork' and 'publicwork_jr' can access add_frequency"""
    center = center_factory.create()
    seeker = create_seeker(center=center)
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("add_frequency", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__update_frequency__by_user_type(
    center_factory,
    create_lecture,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' and 'publicwork_jr' can access update_frequency"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    lecture = create_lecture(center=center)
    lecture.listeners.add(seeker)
    frequency = lecture.listeners.first()
    url = reverse("update_frequency", args=[seeker.pk, frequency.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__remove_frequency__by_user_type(
    center_factory,
    create_lecture,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' and 'publicwork_jr' can access remove_frequency"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    lecture = create_lecture(center=center)
    lecture.listeners.add(seeker)
    frequency = lecture.listeners.first()
    url = reverse("remove_frequency", args=[seeker.pk, frequency.pk])
    response = client.get(url)
    assert response.status_code == status_code
