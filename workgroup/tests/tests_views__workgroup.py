import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


#  Workgroup  #################################################################
@pytest.mark.django_db
def test_unlogged_user_cannot_access_workgroup(db, client):
    url = reverse("workgroup_home")
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_pre__200"]
)
def test_access__workgroup_home__user_by_type(
    auto_login_user, user_type, status_code
):
    """only 'office' and 'presidium' can access workgroup_home"""
    client, user = auto_login_user(group=user_type)
    url = reverse("workgroup_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_pre__200"]
)
def test_access__workgroup_detail__user_by_type(
    auto_login_user, create_workgroup, user_type, status_code
):
    """only 'office' and 'presidium' can access workgroup_detail"""
    client, user = auto_login_user(group=user_type)
    workgroup = create_workgroup()
    url = reverse("workgroup_detail", args=[workgroup.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__workgroup_create__user_by_type(
    auto_login_user, user_type, status_code
):
    """only 'office' can access workgroup_create"""
    client, user = auto_login_user(group=user_type)
    url = reverse("workgroup_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__workgroup_update__user_by_type(
    auto_login_user, create_workgroup, user_type, status_code
):
    """only 'office' can access workgroup_update"""
    client, user = auto_login_user(group=user_type)
    workgroup = create_workgroup()
    url = reverse("workgroup_update", args=[workgroup.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__workgroup_delete__user_by_type(
    auto_login_user, create_workgroup, user_type, status_code
):
    """only 'office' can access workgroup_delete"""
    client, user = auto_login_user(group=user_type)
    workgroup = create_workgroup()
    url = reverse("workgroup_delete", args=[workgroup.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_pre__200"]
)
def test_access__search_workgroup__user_by_type(
    auto_login_user, user_type, status_code
):
    """only 'office' and 'presidium' can search groups"""
    client, user = auto_login_user(group=user_type)
    url = reverse("workgroup_home")
    response = client.get(f"{url}?term=Three&all=on")
    assert response.status_code == status_code
