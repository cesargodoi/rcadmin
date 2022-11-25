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
    ],
)
def test_unlogged_user_cannot_view_lecture_page(create_lecture, client, _type):
    """unlogged user can't access any page of lecture"""
    lecture = create_lecture()
    page = f"lecture_{_type}"
    if _type not in ("home", "create"):
        url = reverse(page, args=[str(lecture.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__lecture_home__by_user_type(
    center_factory, auto_login_user, user_type, status_code
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium' can access lecture_home
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("lecture_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__lecture_detail__by_user_type(
    center_factory,
    create_lecture,
    auto_login_user,
    user_type,
    status_code,
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium'
    can access lecture_detail
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    lecture = create_lecture(center=center)
    url = reverse("lecture_detail", args=[lecture.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("publicwork", 404), ("publicwork_jr", 404), ("presidium", 404)],
)
def test_access_from_other_center__lecture_detail__by_user_type(
    center_factory,
    create_user,
    create_center,
    create_lecture,
    auto_login_user,
    user_type,
    status_code,
):
    """
    the 'publicwork', 'publicwork_jr' and 'presidium' cannot access
    lecture_detail from other center
    """
    center = center_factory.create()
    lecture = create_lecture(center=center, email="s1@um.com")
    other_center = create_center(
        name="Other Center", user=create_user(email="u2@mail.com")
    )
    client, user = auto_login_user(group=user_type, center=other_center)
    url = reverse("lecture_detail", args=[lecture.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__lecture_create__by_user_type(
    center_factory,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access lecture_create"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("lecture_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__lecture_update__by_user_type(
    center_factory,
    create_lecture,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access lecture_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    lecture = create_lecture(center=center)
    url = reverse("lecture_update", args=[lecture.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__lecture_delete__by_user_type(
    center_factory,
    create_lecture,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access lecture_delete view"""
    center = center_factory.create()
    lecture = create_lecture(center=center)
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("lecture_delete", args=[lecture.pk])
    response = client.get(url)
    assert response.status_code == status_code
