import pytest
from django.urls import reverse

from event.models import Frequency
from rcadmin.permissions_for_tests import permission


#  Workgroup  #################################################################
@pytest.mark.django_db
def test_unlogged_user_cannot_access_mentoring(db, client):
    url = reverse("mentoring_home")
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__mentoring_home__user_by_type(
    center_factory, auto_login_user, user_type, status_code
):
    """only 'mentoring' can access workgroup_home"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("mentoring_home")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__mentoring_group_detail__user_by_type(
    center_factory, auto_login_user, create_workgroup, user_type, status_code
):
    """only 'mentoring' can access mentoring_group_detail"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    workgroup = create_workgroup(center=center)
    url = reverse("mentoring_group_detail", args=[workgroup.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__mentoring_group_frequencies__user_by_type(
    center_factory, auto_login_user, create_workgroup, user_type, status_code
):
    """only 'mentoring' can access mentoring_group_frequencies"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    workgroup = create_workgroup(center=center)
    url = reverse("mentoring_group_frequencies", args=[workgroup.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__mentoring_member_detail__user_by_type(
    center_factory,
    auto_login_user,
    create_workgroup,
    create_person,
    user_type,
    status_code,
):
    """only 'mentoring' can access mentoring_member_detail"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    workgroup = create_workgroup(center=center)
    workgroup.members.add(person)
    url = reverse("mentoring_member_detail", args=[workgroup.pk, person.id])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__mentoring_member_frequencies__user_by_type(
    center_factory,
    auto_login_user,
    create_workgroup,
    create_person,
    user_type,
    status_code,
):
    """only 'mentoring' can access mentoring_member_frequencies"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    workgroup = create_workgroup(center=center)
    workgroup.members.add(person)
    url = reverse(
        "mentoring_member_frequencies", args=[workgroup.pk, person.id]
    )
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__mentoring_member_historic__user_by_type(
    center_factory,
    auto_login_user,
    create_workgroup,
    create_person,
    user_type,
    status_code,
):
    """only 'mentoring' can access mentoring_member_historic"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    workgroup = create_workgroup(center=center)
    workgroup.members.add(person)
    url = reverse("mentoring_member_historic", args=[workgroup.pk, person.id])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__mentoring_add_frequencies__user_by_type(
    center_factory,
    auto_login_user,
    create_workgroup,
    user_type,
    status_code,
):
    """only 'mentoring' can access mentoring_add_frequencies"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    workgroup = create_workgroup(center=center)
    url = reverse("mentoring_add_frequencies", args=[workgroup.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__membership_add_frequency__user_by_type(
    center_factory,
    auto_login_user,
    create_workgroup,
    create_person,
    user_type,
    status_code,
):
    """only 'mentoring' can access membership_add_frequency"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    workgroup = create_workgroup(center=center)
    workgroup.members.add(person)
    url = reverse("membership_add_frequency", args=[workgroup.pk, person.id])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__membership_update_frequency__user_by_type(
    center_factory,
    auto_login_user,
    create_workgroup,
    create_person,
    create_event,
    user_type,
    status_code,
):
    """only 'mentoring' can access membership_update_frequency"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    event = create_event(center=center)
    event.frequencies.add(person)
    workgroup = create_workgroup(center=center)
    workgroup.members.add(person)
    freq_id = Frequency.objects.last().id
    url = reverse(
        "membership_update_frequency", args=[workgroup.pk, person.id, freq_id]
    )
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_men__200"])
def test_access__membership_remove_frequency__user_by_type(
    center_factory,
    auto_login_user,
    create_workgroup,
    create_person,
    create_event,
    user_type,
    status_code,
):
    """only 'mentoring' can access membership_remove_frequency"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    person = create_person(center=center)
    event = create_event(center=center)
    event.frequencies.add(person)
    workgroup = create_workgroup(center=center)
    workgroup.members.add(person)
    freq_id = Frequency.objects.last().id
    url = reverse(
        "membership_remove_frequency", args=[workgroup.pk, person.id, freq_id]
    )
    response = client.get(url)
    assert response.status_code == status_code
