import pytest
from django.urls import reverse
from django.contrib.auth.models import Group, Permission


center_home = reverse("center_home")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "_type",
    [("home"), ("detail"), ("create"), ("update"), ("delete")],
)
def test_unlogged_person_cannot_access__center_(center_factory, client, _type):
    """unlogged person cannot access any page of center app"""
    center = center_factory.create()
    page = f"center_{_type}"
    if _type in ("update", "detail", "delete"):
        url = reverse(page, args=[str(center.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 200), ("treasury_jr", 200)],
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
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 200), ("treasury_jr", 200)],
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
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__center_update__by_user_type(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    """'user', 'treasury' and 'treasury_jr' can't access center_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type)
    url = reverse("center_update", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_access__center_update__by_offices_own_center(
    center_factory, auto_login_user
):
    """the 'office' can access center_update of only own center"""
    center = center_factory.create()
    client, user = auto_login_user(group="office", center=center)
    url = reverse("center_update", args=[center.pk])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 302), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__center_create__by_user_type(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    """
    'user', 'office', 'treasury' and treasury_jr can't access center_create
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type)
    url = reverse("center_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 302), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__center_delete__by_user_type(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    """
    'user', 'office', 'treasury' and treasury_jr can't access center_delete
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type)
    url = reverse("center_delete", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 200), ("treasury_jr", 200)],
)
def test_search__center_home__by_user_types(
    auto_login_user, get_group, user_type, status_code
):
    """the 'oficce', 'treasury' and 'treasury_jr' can search center"""
    client, user = auto_login_user(group=user_type)
    url = "/center/?term=Group"
    response = client.get(url)
    assert response.status_code == status_code
