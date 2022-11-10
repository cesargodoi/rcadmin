import pytest
from django.urls import reverse

_user = dict(email="basic_user@gmail.com", password="$536wen.")


@pytest.mark.django_db
def test_user_logged_out_can_not_access__profile(auto_login_user):
    client, user = auto_login_user()
    response = client.get(reverse("profile_detail"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_logged_in_can_access__profile(auto_login_user, get_group):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("profile_detail"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access__updt_profile(auto_login_user, get_group):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("updt_profile"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access__updt_image(auto_login_user, get_group):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("updt_image"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access__user_historic(auto_login_user, get_group):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("user_historic"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access__user_payments(
    center_factory, auto_login_user
):
    center = center_factory.create()
    client, user = auto_login_user(group="user", center=center)
    response = client.get(reverse("user_payments"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access__user_payments_neworder(
    center_factory, auto_login_user
):
    center = center_factory.create()
    client, user = auto_login_user(group="user", center=center)
    response = client.get(reverse("user_new_order"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access__user_frequencies(
    auto_login_user, get_group
):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("user_frequencies"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logged_in_can_access__user_frequencies_scan_qrcode(
    auto_login_user, get_group
):
    client, user = auto_login_user()
    user.groups.add(get_group("user"))
    response = client.get(reverse("scan_qrcode_event"))
    assert response.status_code == 200
