import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


#  Membership  ################################################################
@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__membership_insert__user_by_type(
    auto_login_user, create_workgroup, user_type, status_code
):
    """only 'office' can access membership_insert"""
    client, user = auto_login_user(group=user_type)
    workgroup = create_workgroup()
    url = reverse("membership_insert", args=[workgroup.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__membership_update__user_by_type(
    auto_login_user,
    center_factory,
    create_workgroup,
    create_person,
    user_type,
    status_code,
):
    """only 'office' can access membership_update"""
    client, user = auto_login_user(group=user_type)
    center = center_factory.create()
    workgroup = create_workgroup(center=center)
    workgroup.members.add(create_person(email="user@email.com", center=center))
    url = reverse("membership_update", args=[workgroup.id, 1])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__membership_delete__user_by_type(
    auto_login_user,
    center_factory,
    create_workgroup,
    create_person,
    user_type,
    status_code,
):
    """only 'office' can access membership_delete"""
    client, user = auto_login_user(group=user_type)
    center = center_factory.create()
    workgroup = create_workgroup(center=center)
    workgroup.members.add(create_person(email="user@email.com", center=center))
    url = reverse("membership_delete", args=[workgroup.id, 1])
    response = client.get(url)
    assert response.status_code == status_code
