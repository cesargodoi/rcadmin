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
        ("update_info"),
        ("update_others"),
        ("update_image"),
        ("delete"),
    ],
)
def test_unlogged_person_cannot_access__center_(center_factory, client, _type):
    """unlogged person cannot access any page of center app"""
    center = center_factory.create()
    page = f"center_{_type}"
    if _type in (
        "update_info",
        "update_others",
        "update_image",
        "detail",
        "delete",
    ):
        url = reverse(page, args=[str(center.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_tre_trej_pre__200"]
)
def test_access__center_home__by_user_type(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    """only 'user' can't access center_home"""
    center_factory.create()
    client, user = auto_login_user(group=user_type)
    url = reverse("center_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_tre_trej_pre__200"]
)
def test_access__center_detail__by_user_type(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    """
    only 'user' can't access center_detail
    PS - Here we found a problem unsoved with 'treasury' and 'treasury_jr'.
         In manual test, this problem do not appears.
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type)
    url = reverse("center_detail", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_off__404"])
def test_access__center_update__by_user_type(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    """
    'user', 'treasury', 'treasury_jr', 'publicwork', 'publicwork_jr' and
    'presidium' can't access center_updates and gets 302, 'office' gets 404
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type)
    for update in ["update_info", "update_others", "update_image"]:
        url = reverse(f"center_{update}", args=[center.pk])
        response = client.get(url)
        assert response.status_code == status_code


@pytest.mark.django_db
def test_access__center_update__by_offices_own_center(
    center_factory, auto_login_user
):
    """the 'office' can access center_update of only own center"""
    center = center_factory.create()
    client, user = auto_login_user(group="office", center=center)
    for update in ["update_info", "update_others", "update_image"]:
        url = reverse(f"center_{update}", args=[center.pk])
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm__200"])
def test_access__center_create__by_user_type(
    center_factory, auto_login_user, user_type, status_code
):
    """only 'admin' can access center_create"""
    center_factory.create()
    client, user = auto_login_user(group=user_type)
    url = reverse("center_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm__200"])
def test_access__center_delete__by_user_type(
    center_factory, auto_login_user, user_type, status_code
):
    """only 'admin' can access center_delete"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type)
    url = reverse("center_delete", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_off_tre_trej_pre__200"]
)
def test_search__center_home__by_user_types(
    auto_login_user, user_type, status_code
):
    """the 'oficce', 'treasury' and 'treasury_jr' can search center"""
    client, user = auto_login_user(group=user_type)
    url = "/center/?term=Group"
    response = client.get(url)
    assert response.status_code == status_code
