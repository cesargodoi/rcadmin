import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


@pytest.mark.django_db
@pytest.mark.parametrize(
    "_url",
    [
        ("frequencies_per_period"),
        ("lectures_per_period"),
        ("status_per_center"),
    ],
)
def test_unlogged_user_cannot_view_report_page(create_lecture, client, _url):
    """unlogged user can't access any page of report"""
    response = client.get(reverse(_url))
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__frequencies_per_period__by_user_type(
    center_factory, auto_login_user, user_type, status_code
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium'
    can access frequencies_per_period
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("frequencies_per_period")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__lectures_per_period__by_user_type(
    center_factory, auto_login_user, user_type, status_code
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium'
    can access lectures_per_period
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("lectures_per_period")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__status_per_center__by_user_type(
    center_factory, auto_login_user, user_type, status_code
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium'
    can access status_per_center
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("status_per_center")
    response = client.get(url)
    assert response.status_code == status_code
