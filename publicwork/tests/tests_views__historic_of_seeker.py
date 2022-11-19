import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


@pytest.mark.django_db
@pytest.mark.parametrize(
    "_type",
    [("create"), ("update"), ("delete")],
)
def test_unlogged_user_cannot_add_update_delete_historic(
    center_factory, create_seeker, client, _type
):
    """
    unlogged user can't access
    'create_historic', 'update_historic', 'delete_historic'
    """
    center = center_factory.create()
    seeker = create_seeker(center=center)
    page = f"{_type}_historic"
    if _type == "create":
        url = reverse(page, args=[str(seeker.pk)])
    else:
        url = reverse(page, args=[str(seeker.pk), str(seeker.pk)])
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__create_historic__by_user_type(
    center_factory, create_seeker, auto_login_user, user_type, status_code
):
    """only 'publicwork' and 'publicwork_jr' can access create_historic"""
    center = center_factory.create()
    seeker = create_seeker(center=center)
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("create_historic", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__update_historic__by_user_type(
    center_factory,
    create_seeker,
    create_historic_of_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' and 'publicwork_jr' can access update_historic"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    historic = create_historic_of_seeker(seeker=seeker)
    url = reverse("update_historic", args=[seeker.pk, historic.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__delete_historic__by_user_type(
    center_factory,
    create_seeker,
    create_historic_of_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' and 'publicwork_jr' can access delete_historic"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    historic = create_historic_of_seeker(seeker=seeker)
    url = reverse("delete_historic", args=[seeker.pk, historic.pk])
    response = client.get(url)
    assert response.status_code == status_code
