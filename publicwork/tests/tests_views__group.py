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
    ],
)
def test_unlogged_user_cannot_view_group_page(create_lecture, client, _type):
    """unlogged user can't access any page of group"""
    lecture = create_lecture()
    page = f"group_{_type}"
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
def test_access__group_home__by_user_type(
    center_factory, auto_login_user, user_type, status_code
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium' can access group_home
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("group_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj_pre__200"]
)
def test_access__group_detail__by_user_type(
    center_factory,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """
    only 'publicwork', 'publicwork_jr' and 'presidium'
    can access group_detail
    """
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    publicwork_group = create_publicwork_group(center=center)
    url = reverse("group_detail", args=[publicwork_group.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.actual
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("publicwork", 404), ("publicwork_jr", 404), ("presidium", 404)],
)
def test_access_from_other_center__group_detail__by_user_type(
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
    group_detail from other center
    """
    center = center_factory.create()
    lecture = create_lecture(center=center, email="s1@um.com")
    other_center = create_center(
        name="Other Center", user=create_user(email="u2@mail.com")
    )
    client, user = auto_login_user(group=user_type, center=other_center)
    url = reverse("group_detail", args=[lecture.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__group_create__by_user_type(
    center_factory,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_create"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("group_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__group_update__by_user_type(
    center_factory,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    publicwork_group = create_publicwork_group(center=center)
    url = reverse("group_update", args=[publicwork_group.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__group_delete__by_user_type(
    center_factory,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_delete"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    publicwork_group = create_publicwork_group(center=center)
    url = reverse("group_delete", args=[publicwork_group.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__group_reinsert__by_user_type(
    center_factory,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_reinsert"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    publicwork_group = create_publicwork_group(center=center)
    url = reverse("group_reinsert", args=[publicwork_group.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__group_frequencies__by_user_type(
    center_factory,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_frequencies"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    publicwork_group = create_publicwork_group(center=center)
    url = reverse("group_frequencies", args=[publicwork_group.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_pub_pubj__200"]
)
def test_access__group_add_frequencies__by_user_type(
    center_factory,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_add_frequencies"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    publicwork_group = create_publicwork_group(center=center)
    url = reverse("group_add_frequencies", args=[publicwork_group.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__group_add_member__by_user_type(
    center_factory,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_add_member"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    publicwork_group = create_publicwork_group(center=center)
    url = reverse("group_add_member", args=[publicwork_group.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__group_remove_member__by_user_type(
    center_factory,
    create_seeker,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_remove_member"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    seeker = create_seeker(center=center)
    publicwork_group = create_publicwork_group(center=center)
    publicwork_group.members.add(seeker)
    url = reverse("group_remove_member", args=[publicwork_group.pk, seeker.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__group_add_mentor__by_user_type(
    center_factory,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_add_mentor"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    publicwork_group = create_publicwork_group(center=center)
    url = reverse("group_add_mentor", args=[publicwork_group.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_pub__200"])
def test_access__group_remove_mentor__by_user_type(
    center_factory,
    create_person,
    create_publicwork_group,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'publicwork' can access group_remove_mentor"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    publicwork_group = create_publicwork_group(center=center)
    publicwork_group.mentors.add(person)
    url = reverse("group_remove_mentor", args=[publicwork_group.pk, person.pk])
    response = client.get(url)
    assert response.status_code == status_code
