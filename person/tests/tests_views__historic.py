import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


#  Historic  ##################################################################
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_pre__200"]
)
def test_access__person_historic__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'admin' and 'office' can access person_historic"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    url = reverse("person_historic", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__historic_create__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'admin' and 'office' can access historic_create"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    url = reverse("historic_create", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__historic_update__by_user_type(
    center_factory,
    create_person,
    create_historic,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'admin' and 'office' can access historic_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    create_historic(person)
    url = reverse("historic_update", args=[person.pk, 1])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__historic_delete__by_user_type(
    center_factory,
    create_person,
    create_historic,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'admin' and 'office' can access historic_delete"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    create_historic(person)
    url = reverse("historic_delete", args=[person.pk, 1])
    response = client.get(url)
    assert response.status_code == status_code


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
    """only 'admin' and 'office' can access invitations"""
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
    """only 'admin' and 'office' can access invite_person"""
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
    """only 'admin' and 'office' can access remove_invite"""
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
    """only 'admin' and 'office' can access resend_invitation"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    invite = create_invitation(center)
    url = reverse("resend_invitation", args=[invite.pk])
    response = client.get(url)
    assert response.status_code == status_code
