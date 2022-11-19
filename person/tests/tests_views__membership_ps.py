import pytest

from django.urls import reverse

from rcadmin.permissions_for_tests import permission


#  membership_ps_view  ########################################################
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_pre__200"]
)
def test_access__membership_ps_list__by_user_type(
    create_center,
    create_user,
    create_workgroup,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    center = create_center(user=create_user(email="u2@mail.com"))
    workgroup = create_workgroup(center=center)
    person = create_person(center=center, email="b@b.com")
    workgroup.members.add(person)

    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("membership_ps_list", args=[person.id])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__membership_ps_create__by_user_type(
    create_center,
    create_user,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    center = create_center(user=create_user(email="u2@mail.com"))
    person = create_person(center=center, email="a@a.com")

    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("membership_ps_create", args=[person.id])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__membership_ps_update__by_user_type(
    create_center,
    create_user,
    create_workgroup,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    center = create_center(user=create_user(email="u2@mail.com"))
    workgroup = create_workgroup(center=center)
    person = create_person(center=center, email="a@a.com")
    workgroup.members.add(person)

    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("membership_ps_update", args=[person.id, workgroup.id])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__membership_ps_delete__by_user_type(
    create_center,
    create_user,
    create_workgroup,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    center = create_center(user=create_user(email="u2@mail.com"))
    workgroup = create_workgroup(center=center)
    person = create_person(center=center, email="a@a.com")
    workgroup.members.add(person)

    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("membership_ps_delete", args=[person.id, workgroup.id])
    response = client.get(url)
    assert response.status_code == status_code
