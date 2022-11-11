import pytest
from django.contrib import auth
from user.models import User


@pytest.mark.django_db
def test_user_dont_get_logged_in(client):
    client.login(email="outsider@gmail.com", password="$536wen.")
    user = auth.get_user(client)
    assert user.is_authenticated is False


@pytest.mark.django_db
def test_add_new_user_and_try_to_login(client, auto_login_user):
    client, user = auto_login_user()
    assert user.is_authenticated


@pytest.mark.django_db
def test_user_get_logged_out(client, auto_login_user):
    client, user = auto_login_user()
    client.logout()
    user = auth.get_user(client)
    assert user.is_authenticated is False


new_user = dict(email="new@user.com", password="secret")


@pytest.mark.django_db
def test_add_new_user(create_user):
    create_user(**new_user)
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_verify_if_profile_is_created(create_user):
    user = create_user(**new_user)
    assert user.profile.social_name.startswith("<<")


@pytest.mark.django_db
def test_verify_if_person_is_created(create_user):
    user = create_user(**new_user)
    assert "new" in user.person.name


@pytest.mark.django_db
def test_edit_user(create_user):
    create_user()
    user = User.objects.last()
    user.email = "edited@user.com"
    user.save()
    edited_user = User.objects.last()
    assert edited_user.email == "edited@user.com"


@pytest.mark.django_db
def test_delete_user(create_user):
    create_user(**new_user)
    user = User.objects.last()
    user.delete()
    assert User.objects.count() == 0
