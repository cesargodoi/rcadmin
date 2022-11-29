import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


@pytest.mark.django_db
@pytest.mark.parametrize(
    "_type",
    [
        ("home"),
        ("detail"),
        ("create"),
        ("update_profile"),
        ("update_pupil"),
        ("update_image"),
        ("delete"),
        ("reinsert"),
    ],
)
def test_unlogged_person_cannot_view_person_page(create_person, client, _type):
    """unlogged person can't access any page of person app"""
    person = create_person()
    page = f"person_{_type}"
    if _type in ("detail", "delete", "reinsert"):
        url = reverse(page, args=[str(person.pk)])
    elif _type in ("update_profile", "update_pupil", "update_image"):
        url = reverse(_type, args=[str(person.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_pre__200"]
)
def test_access__person_home__by_user_type(
    auto_login_user, get_group, user_type, status_code
):
    """only 'office' can access person_home"""
    client, user = auto_login_user(group=user_type)
    url = reverse("person_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_pre__200"]
)
def test_access__person_detail__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access person_detail"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    url = reverse("person_detail", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_access_office_cannot_access__person_detail__from_other_center(
    center_factory, create_user, create_center, create_person, auto_login_user
):
    """the 'office' can't access person_detail from other center"""
    center = center_factory.create()
    person = create_person(center=center, email="p1@um.com")
    other_center = create_center(
        name="Other Center", user=create_user(email="u2@mail.com")
    )
    client, user = auto_login_user(group="office", center=other_center)
    url = reverse("person_detail", args=[person.pk])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["all__302"])
def test_access__person_create__by_user_type(
    center_factory,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'superuser' can access person_create"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("person_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__person_update__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access person_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    for update in ["update_profile", "update_pupil", "update_image"]:
        url = reverse(update, args=[person.pk])
        response = client.get(url)
        assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__person_delete__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access person_delete view"""
    center = center_factory.create()
    person = create_person(center=center)
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("person_delete", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_pre__200"]
)
def test_search_persons_by_user_type(auto_login_user, user_type, status_code):
    """only 'admin', 'office' and 'presidium' can search persons"""
    client, user = auto_login_user(group=user_type)
    url = "/person/?ps_term=cesar&all=on"
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__person_reinsert__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access person_reinsert view"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    url = reverse("person_reinsert", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code
