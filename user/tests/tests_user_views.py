import pytest
from django.urls import reverse

_user = dict(email="basic_user@gmail.com", password="$536wen.")


@pytest.mark.django_db
def test_user_logged_out_can_not_access_profile(auto_login_user):
    client, user = auto_login_user()
    response = client.get(reverse("profile_detail"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_logged_in_can_access_profile(auto_login_user, get_group):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("profile_detail"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access_edit_profile(auto_login_user, get_group):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("profile_update"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access_user_historic(auto_login_user, get_group):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("user_historic"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access_user_payments(auto_login_user, get_group):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("user_payments"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access_user_payments_neworder(
    auto_login_user, get_group
):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("user_new_order"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access_user_frequencies(
    auto_login_user, get_group
):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("user_frequencies"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access_user_frequencies_scan_qrcode(
    auto_login_user, get_group
):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("scan_qrcode_event"))
    assert response.status_code == 200
