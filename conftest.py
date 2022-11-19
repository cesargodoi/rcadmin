import random
import pytest

from django.utils import timezone
from pytest_factoryboy import register
from django.contrib.auth.models import Group, Permission
from factories import (
    fake,
    UserFactory,
    CenterFactory,
    ActivityFactory,
    PaytypeFactory,
    BankflagFactory,
)
from center.models import Center
from person.models import Person, Historic, Invitation
from event.models import Event
from workgroup.models import Workgroup, Membership
from treasury.models import Payment, FormOfPayment, Order
from publicwork.models import (
    Seeker,
    HistoricOfSeeker,
    Lecture,
    PublicworkGroup,
)
from rcadmin.common import ASPECTS, STATUS, OCCURRENCES, SEEKER_STATUS

register(UserFactory)
register(CenterFactory)
register(ActivityFactory)
register(PaytypeFactory)
register(BankflagFactory)


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
def create_center(db, create_user):
    def make_center(**kwargs):
        new = dict(
            name=kwargs.get("name")
            or f"Center {fake.pyint(min_value=1, max_value=100)}",
            city=fake.city(),
            state=fake.estado_sigla(),
            country=fake.current_country_code(),
            phone_1=fake.phone_number(),
            email=kwargs.get("email") or fake.email(),
            center_type="CNT",
            mentoring=True,
            treasury=True,
            publicwork=True,
            accommodation=True,
            made_by=kwargs.get("user") or create_user(),
        )
        return Center.objects.create(**new)

    return make_center


@pytest.fixture
def auto_login_user(db, client, create_user, get_password, get_group):
    def make_auto_login(**kwargs):
        new_user = kwargs.get("user") or create_user()

        if kwargs.get("group"):
            new_user.groups.add(get_group(kwargs.get("group")))
        if kwargs.get("center"):
            kwargs.get("center").person_set.add(new_user.person)

        client.login(email=new_user.email, password=get_password)
        return client, new_user

    return make_auto_login


@pytest.fixture
def create_person(db, create_user, center_factory):
    def make_person(**kwargs):
        user = create_user(email=kwargs.get("email"))

        person = Person.objects.get(user=user)
        person.name = kwargs.get("name") or fake.name()
        person.center = kwargs.get("center") or center_factory.create()
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
        new = dict(
            person=person,
            occurrence=occur if occur else random.choice(OCCURRENCES),
            date=fake.date_between(start_date="-1y", end_date="today"),
        )

        historic = Historic.objects.create(**new)
        return historic

    return make_historic


@pytest.fixture
def create_invitation(db):
    def make_invitation(center):
        new = dict(
            center=center,
            name=fake.name(),
            email=fake.email(),
            birth=fake.date_between(start_date="-38y", end_date="-18y"),
            id_card=fake.cpf(),
        )

        invitation = Invitation.objects.create(**new)
        return invitation

    return make_invitation


@pytest.fixture
def create_event(db, activity_factory, center_factory, create_user):
    def make_event(**kwargs):
        center = kwargs.get("center") or center_factory()
        activity = kwargs.get("activity") or activity_factory()

        new_event = dict(
            center=center,
            activity=activity,
            date=timezone.now(),
            status="OPN",
            made_by=create_user(),
        )

        event = Event(**new_event)
        event.save()
        return event

    return make_event


@pytest.fixture
def create_frequency(
    db, create_event, create_person, activity_factory, center_factory
):
    def make_frequency(**kwargs):
        center = kwargs.get("center") or center_factory()
        activity = kwargs.get("activity") or activity_factory()

        if Event.objects.filter(center=center, activity=activity):
            event = Event.objects.filter(
                center=center, activity=activity
            ).first()
        else:
            event = kwargs.get("event") or create_event(
                center=center, activity=activity
            )

        _person = kwargs.get("person") or create_person(center=center)

        frequency = event.frequency_set.create(person=_person)
        return frequency

    return make_frequency


@pytest.fixture
def create_workgroup(db, create_user, center_factory):
    def make_workgroup(**kwargs):
        new = dict(
            name=kwargs.get("name")
            or f"Group_{fake.pyint(min_value=1, max_value=9)}",
            center=kwargs.get("center") or center_factory(),
            workgroup_type=kwargs.get("workgroup_type") or "MNT",
            aspect=kwargs.get("aspect") or "",
            made_by=create_user(),
        )

        workgroup = Workgroup.objects.create(**new)
        return workgroup

    return make_workgroup


@pytest.fixture
def create_membership(db, create_person, create_workgroup):
    def make_membership(**kwargs):
        new = dict(
            person=kwargs.get("person")
            or create_person(center=kwargs.get("center")),
            workgroup=kwargs.get("workgroup")
            or create_workgroup(center=kwargs.get("center")),
            role_type=kwargs.get("role_type") or "MBR",
        )

        membership = Membership.objects.create(**new)
        return membership

    return make_membership


@pytest.fixture
def create_payment(db, paytype_factory, create_person):
    def make_payment(**kwargs):
        new = dict(
            paytype=paytype_factory.create(),
            person=kwargs.get("person")
            or create_person(center=kwargs.get("center")),
            event=kwargs.get("event") or None,
            ref_month=kwargs.get("ref_month") or fake.date(),
            value=kwargs.get("value") or 120,
        )

        payment = Payment.objects.create(**new)
        return payment

    return make_payment


@pytest.fixture
def create_form_of_payment(db, bankflag_factory):
    def make_form_of_payment(**kwargs):
        new = dict(
            payform_type=kwargs.get("type") or "CSH",
            bank_flag=kwargs.get("bank_flag") or bankflag_factory.create(),
            value=kwargs.get("value") or 120,
        )

        form_of_payment = FormOfPayment.objects.create(**new)
        return form_of_payment

    return make_form_of_payment


@pytest.fixture
def create_order(
    db, center_factory, create_person, create_payment, create_form_of_payment
):
    def make_order(**kwargs):
        center = kwargs.get("center") or center_factory()
        person = kwargs.get("person") or create_person(center=center)
        new = dict(
            center=center,
            person=person,
            amount=kwargs.get("amount") or 120,
            status=kwargs.get("status") or "PND",
        )

        order = Order.objects.create(**new)
        order.payments.add(
            kwargs.get("payment") or create_payment(person=person)
        )
        order.form_of_payments.add(
            kwargs.get("form_of_payment") or create_form_of_payment()
        )
        return order

    return make_order


@pytest.fixture
def create_seeker(db, center_factory):
    def make_seeker(**kwargs):
        new = dict(
            center=kwargs.get("center") or center_factory.create(),
            name=kwargs.get("name") or fake.name(),
            birth=kwargs.get("birth") or fake.date_of_birth(maximum_age=80),
            gender=kwargs.get("gender") or random.choice(["M", "F"]),
            city=kwargs.get("city") or fake.city(),
            state=kwargs.get("state") or fake.state(),
            country=kwargs.get("country") or fake.country(),
            email=kwargs.get("email") or fake.email(),
        )
        seeker = Seeker.objects.create(**new)
        return seeker

    return make_seeker


@pytest.fixture
def create_historic_of_seeker(db, create_seeker):
    def make_historic(**kwargs):
        new = dict(
            seeker=kwargs.get("seeker") or create_seeker(),
            occurrence=kwargs.get("occurrence")
            or random.choice([occ[0] for occ in SEEKER_STATUS]),
            date=kwargs.get("date") or timezone.now().date(),
        )
        historic = HistoricOfSeeker.objects.create(**new)
        return historic

    return make_historic


@pytest.fixture
def create_lecture(db, center_factory):
    def make_lecture(**kwargs):
        new = dict(
            center=kwargs.get("center") or center_factory.create(),
            theme=kwargs.get("theme")
            or f"Theme_{fake.pyint(min_value=1, max_value=9)}",
            date=kwargs.get("date") or timezone.now().date(),
        )
        lecture = Lecture.objects.create(**new)
        return lecture

    return make_lecture


@pytest.fixture
def create_publicwork_group(db, center_factory):
    def make_publicwork_group(**kwargs):
        center = kwargs.get("center") or center_factory.create()
        new = dict(
            name=kwargs.get("name")
            or f"Publicwork_Group_{fake.pyint(min_value=1, max_value=9)}",
            center=center,
            made_by=center.made_by,
        )
        publicwork_group = PublicworkGroup.objects.create(**new)
        publicwork_group.mentors.set(kwargs.get("mentors") or [])
        publicwork_group.members.set(kwargs.get("members") or [])

        return publicwork_group

    return make_publicwork_group


###############################################################################


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
    user = [
        "view_user",  # user
        "change_user",
        "view_profile",  # profile
        "change_profile",
    ]
    office = [
        "view_center",  # center
        "change_center",
        "add_event",  # event
        "change_event",
        "delete_event",
        "view_event",
        "add_frequency",  # frequency
        "change_frequency",
        "delete_frequency",
        "view_frequency",
        "add_historic",  # historic
        "change_historic",
        "delete_historic",
        "view_historic",
        "add_person",  # person
        "change_person",
        "delete_person",
        "view_person",
        "add_invitation",  # invitation
        "change_invitation",
        "delete_invitation",
        "view_invitation",
        "add_membership",  # membership
        "change_membership",
        "delete_membership",
        "view_membership",
        "add_workgroup",  # workgroup
        "change_workgroup",
        "delete_workgroup",
        "view_workgroup",
    ]
    mentoring = [
        "view_workgroup",
    ]
    treasury = [
        "view_center",  # center
        "add_order",  # orde
        "change_order",
        "delete_order",
        "view_order",
    ]
    treasury_jr = [
        "view_center",  # center
        "add_order",  # order
        "view_order",
    ]
    publicwork = [
        "change_seeker",  # seeker
        "delete_seeker",
        "view_seeker",
        "add_publicworkgroup",  # publicwork_group
        "change_publicworkgroup",
        "delete_publicworkgroup",
        "view_publicworkgroup",
        "add_historicofseeker",  # historic
        "change_historicofseeker",
        "delete_historicofseeker",
        "view_historicofseeker",
        "add_lecture",  # lecture
        "change_lecture",
        "delete_lecture",
        "view_lecture",
        "add_listener",  # listener
        "change_listener",
        "delete_listener",
        "view_listener",
    ]
    publicwork_jr = [
        "change_seeker",  # seeker
        "view_seeker",
        "view_publicworkgroup",  # publicwork_group
        "add_historicofseeker",  # historic
        "change_historicofseeker",
        "delete_historicofseeker",
        "view_historicofseeker",
        "view_lecture",  # lecture
        "add_listener",  # listener
        "change_listener",
        "delete_listener",
        "view_listener",
    ]
    presidium = [
        "view_center",  # center
        "view_event",  # event
        "view_frequency",  # frequency
        "view_historic",  # historic
        "view_person",  # person
        "view_membership",  # membership
        "view_workgroup",  # workgroup
        "view_seeker",  # publicwork
        "view_historicofseeker",
        "view_lecture",
        "view_listener",
        "view_publicworkgroup",
    ]

    perms = {
        "admin": [perm for perm in Permission.objects.all()],
        "user": [Permission.objects.get(codename=perm) for perm in user],
        "office": [Permission.objects.get(codename=perm) for perm in office],
        "mentoring": [
            Permission.objects.get(codename=perm) for perm in mentoring
        ],
        "treasury": [
            Permission.objects.get(codename=perm) for perm in treasury
        ],
        "treasury_jr": [
            Permission.objects.get(codename=perm) for perm in treasury_jr
        ],
        "publicwork": [
            Permission.objects.get(codename=perm) for perm in publicwork
        ],
        "publicwork_jr": [
            Permission.objects.get(codename=perm) for perm in publicwork_jr
        ],
        "presidium": [
            Permission.objects.get(codename=perm) for perm in presidium
        ],
    }

    return perms
