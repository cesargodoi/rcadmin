import pytest
from django.urls import reverse


#  Person  ####################################################################
@pytest.mark.django_db
@pytest.mark.parametrize(
    "_type",
    [("home"), ("detail"), ("create"), ("update"), ("delete"), ("reinsert")],
)
def test_unlogged_person_cannot_view_center_page(create_person, client, _type):
    """unlogged person can't access any page of person app"""
    person = create_person()
    page = f"person_{_type}"
    if _type in ("update", "detail", "delete", "reinsert"):
        url = reverse(page, args=[str(person.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
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
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
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


@pytest.mark.skip
@pytest.mark.django_db
def test_access_office_cannot_access__person_detail__from_other_center(
    center_factory, create_person, auto_login_user
):
    """the 'office' can't access person_detail from other center"""
    # center, other_center = center_factory.create_batch(2)
    # client, user = auto_login_user(group="office", center=center)
    # person = create_person(center=other_center)
    # url = reverse("person_detail", args=[person.pk])
    # response = client.get(url)
    # assert response.status_code == 404
    ...


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__person_create__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access person_create"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("person_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
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
    url = reverse("person_update", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__person_delete__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access person_delete view"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    url = reverse("person_delete", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
def test_search_persons_by_user_type(
    auto_login_user, get_group, user_type, status_code
):
    """only 'office' can search persons"""
    client, user = auto_login_user(group=user_type)
    url = "/person/?ps_term=cesar&all=on"
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
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


#  Historic  ##################################################################
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__person_historic__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access person_historic"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    url = reverse("person_historic", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__historic_create__by_user_type(
    center_factory,
    create_person,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access historic_create"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    url = reverse("historic_create", args=[person.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__historic_update__by_user_type(
    center_factory,
    create_person,
    create_historic,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access historic_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    create_historic(person)
    url = reverse("historic_update", args=[person.pk, 1])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code",
    [("user", 302), ("office", 200), ("treasury", 302), ("treasury_jr", 302)],
)
def test_access__historic_delete__by_user_type(
    center_factory,
    create_person,
    create_historic,
    auto_login_user,
    user_type,
    status_code,
):
    """only 'office' can access historic_delete"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    create_historic(person)
    url = reverse("historic_delete", args=[person.pk, 1])
    response = client.get(url)
    assert response.status_code == status_code


#  frequency_ps_view ##########################################################
@pytest.mark.skip
@pytest.mark.django_db
def test_only_office_logged_in_can_access_frequency_list_in_person():
    ...


@pytest.mark.skip
@pytest.mark.django_db
def test_only_office_logged_in_can_access_frequency_create_in_person():
    ...


@pytest.mark.skip
@pytest.mark.django_db
def test_only_office_logged_in_can_access_frequency_delete_in_person():
    ...


#  membership_ps_view  ########################################################
@pytest.mark.skip
@pytest.mark.django_db
def test_only_office_logged_in_can_access_membership_list_in_person():
    ...


@pytest.mark.skip
@pytest.mark.django_db
def test_only_office_logged_in_can_access_membership_create_in_person():
    ...


@pytest.mark.skip
@pytest.mark.django_db
def test_only_office_logged_in_can_access_membership_delete_in_person():
    ...
