import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


#  Invitation  ################################################################
@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__invitations__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access invitations"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("invitations")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__invite_person__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access invite_person"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("invite_person")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__remove_invite__by_user_type(
    center_factory,
    create_invitation,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access remove_invite"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    invite = create_invitation(center)
    url = reverse("remove_invite", args=[invite.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__resend_invitation__by_user_type(
    center_factory,
    create_invitation,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access resend_invitation"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    invite = create_invitation(center)
    url = reverse("resend_invitation", args=[invite.pk])
    response = client.get(url)
    assert response.status_code == status_code
