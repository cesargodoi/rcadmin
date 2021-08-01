import random
import pytest

from pytest_factoryboy import register
from django.contrib.auth.models import Group, Permission
from factories import (
    fake,
    UserFactory,
    CenterFactory,
    TempRegOfSeeker,
    SeekerFactory,
)
from person.models import Person, Historic
from schooladmin.common import ASPECTS, STATUS, OCCURRENCES

register(UserFactory)
register(CenterFactory)
register(TempRegOfSeeker)
register(SeekerFactory)


@pytest.fixture
def get_password():
    return "secret"


@pytest.fixture
def create_user(db, django_user_model, get_password):
    def make_user(**kwargs):
        kwargs["email"] = kwargs.get("email") or fake.email()
        kwargs["password"] = kwargs.get("password") or get_password
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, get_password, get_group):
    def make_auto_login(user=None, group=None, center=None):
        new_user = user if user else create_user()
        if group:
            new_user.groups.add(get_group(group))
        if center:
            center.person_set.add(new_user.person)
        client.login(email=new_user.email, password=get_password)
        return client, new_user

    return make_auto_login


@pytest.fixture
def create_person(db, create_user, center_factory):
    def make_person(center=None, name=None):
        user = create_user()
        person = Person.objects.get(user=user)
        person.name = name if name else fake.name()
        person.center = center if center else center_factory.create()
        person.birth = fake.date_of_birth(maximum_age=80)
        person.aspect = random.choice(ASPECTS)
        person.aspect_date = fake.date_between(
            start_date="-10y", end_date="today"
        )
        person.status = random.choice(STATUS)
        person.save()
        return person

    return make_person


@pytest.fixture
def create_historic(db):
    def make_historic(person, occur=None):
        new_occur = dict(
            person=person,
            occurrence=occur if occur else random.choice(OCCURRENCES),
            date=fake.date_between(start_date="-1y", end_date="today"),
        )
        historic = Historic.objects.create(**new_occur)
        return historic

    return make_historic


#  Groups and Permissions
@pytest.fixture
def get_group(db, get_perms):
    def make_group(_name):
        group = Group.objects.create(name=_name)
        perms = get_perms[_name]
        group.permissions.set(perms)
        group.save()
        return group

    return make_group


@pytest.fixture
def get_perms(db):
    perms = {
        "user": [
            # user and profile
            Permission.objects.get(codename="view_user"),
            Permission.objects.get(codename="change_user"),
            Permission.objects.get(codename="view_profile"),
            Permission.objects.get(codename="change_profile"),
        ],
        "office": [
            # center
            Permission.objects.get(codename="view_center"),
            Permission.objects.get(codename="change_center"),
            # event
            Permission.objects.get(codename="add_event"),
            Permission.objects.get(codename="change_event"),
            Permission.objects.get(codename="delete_event"),
            Permission.objects.get(codename="view_event"),
            # historic
            Permission.objects.get(codename="add_historic"),
            Permission.objects.get(codename="change_historic"),
            Permission.objects.get(codename="delete_historic"),
            Permission.objects.get(codename="view_historic"),
            # person
            Permission.objects.get(codename="add_person"),
            Permission.objects.get(codename="change_person"),
            Permission.objects.get(codename="delete_person"),
            Permission.objects.get(codename="view_person"),
            # membership
            Permission.objects.get(codename="add_membership"),
            Permission.objects.get(codename="change_membership"),
            Permission.objects.get(codename="delete_membership"),
            Permission.objects.get(codename="view_membership"),
            # workgroup
            Permission.objects.get(codename="add_workgroup"),
            Permission.objects.get(codename="change_workgroup"),
            Permission.objects.get(codename="delete_workgroup"),
            Permission.objects.get(codename="view_workgroup"),
        ],
        "treasury": [
            # center
            Permission.objects.get(codename="view_center"),
            # order
            Permission.objects.get(codename="add_order"),
            Permission.objects.get(codename="change_order"),
            Permission.objects.get(codename="delete_order"),
            Permission.objects.get(codename="view_order"),
        ],
        "treasury_jr": [
            # center
            Permission.objects.get(codename="view_center"),
            # order
            Permission.objects.get(codename="add_order"),
            Permission.objects.get(codename="view_order"),
        ],
    }
    return perms
