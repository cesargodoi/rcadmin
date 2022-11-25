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
        ("update"),
        ("delete"),
        ("reinsert"),
        ("frequencies"),
        ("historic"),
    ],
)
def test_unlogged_user_cannot_view_seeker_page(create_seeker, client, _type):
    """unlogged user can't access any page of seeker"""
    seeker = create_seeker()
    page = f"seeker_{_type}"
    if _type not in ("home", "create"):
        url = reverse(page, args=[str(seeker.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__seeker_home__by_user_type(
    center_factory, auto_login_user, get_group, user_type, status_code
):
    """
    only 'admin', 'publicwork', 'publicwork_jr' and 'presidium'
    can access seeker_home
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("seeker_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__seeker_detail__by_user_type(
    center_factory,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access seeker_detail"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    url = reverse("seeker_detail", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("publicwork", 404), ("publicwork_jr", 404), ("presidium", 404)],
)
def test_access_from_other_center__seeker_detail__by_user_type(
    center_factory,
    create_user,
    create_center,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """
    the 'publicwork', 'publicwork_jr' and 'presidium' cannot access
    seeker_detail from other center
    """
    center = center_factory.create()
    seeker = create_seeker(center=center, email="s1@um.com")
    other_center = create_center(
        name="Other Center", user=create_user(email="u2@mail.com")
    )
    client, user = auto_login_user(group=user_type, center=other_center)
    url = reverse("seeker_detail", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["all__302"])
def test_access__seeker_create__by_user_type(
    center_factory,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'superuser' can access seeker_create"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("seeker_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__seeker_update__by_user_type(
    center_factory,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' and 'publicwork_jr can access seeker_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    url = reverse("seeker_update", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__seeker_delete__by_user_type(
    center_factory,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access seeker_delete view"""
    center = center_factory.create()
    seeker = create_seeker(center=center)
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("seeker_delete", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_search_seekers_by_user_type(
    center_factory, auto_login_user, user_type, status_code
):
    """only 'publicwork', 'publicwork_jr' and 'presidium' can search seekers"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    base = reverse("seeker_home")
    url = "{}?sk_name=cesar&sk_city=&center={}&sk_status=all&all=off".format(
        base, center.id
    )
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__seeker_reinsert__by_user_type(
    center_factory,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access seeker_reinsert view"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    url = reverse("seeker_reinsert", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__seeker_frequencies__by_user_type(
    center_factory,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium' can access
    seeker_frequencies view
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    url = reverse("seeker_frequencies", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__seeker_historic__by_user_type(
    center_factory,
    create_seeker,
    auto_login_user,
    user_type,
    status_code,
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium' can access
    seeker_historic view
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    url = reverse("seeker_historic", args=[seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code
