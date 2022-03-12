import pytest
from event.models import Activity, Event
from person.models import Person


# Activity
@pytest.mark.events
@pytest.mark.django_db
def test_list_activities(activity_factory):
    for _ in range(3):
        activity_factory()
    assert Activity.objects.count() == 3


@pytest.mark.events
@pytest.mark.django_db
def test_create_activity(activity_factory):
    activity_factory()
    assert Activity.objects.count() == 1


@pytest.mark.events
@pytest.mark.django_db
def test_update_activity(activity_factory):
    activity_factory()
    activity = Activity.objects.last()
    activity.multi_date = True
    activity.save()
    assert activity.multi_date is True


@pytest.mark.events
@pytest.mark.django_db
def test_delete_activity(activity_factory):
    for _ in range(3):
        activity_factory()
    Activity.objects.last().delete()
    assert Activity.objects.count() == 2


# events
@pytest.mark.events
@pytest.mark.django_db
def test_list_event(center_factory, create_event):
    _center = center_factory()
    for _ in range(3):
        create_event(center=_center)
    assert Event.objects.count() == 3


@pytest.mark.events
@pytest.mark.django_db
def test_create_event(create_event):
    create_event()
    assert Event.objects.count() == 1


@pytest.mark.events
@pytest.mark.django_db
def test_update_event(create_event):
    create_event()
    event = Event.objects.last()
    event.status = "CLS"
    event.save()
    assert event.status != "OPN"


@pytest.mark.events
@pytest.mark.django_db
def test_delete_event(center_factory, create_event):
    _center = center_factory()
    for _ in range(3):
        create_event(center=_center)
    Event.objects.last().delete()
    assert Event.objects.count() == 2


# frequencies
@pytest.mark.events
@pytest.mark.django_db
def test_list_frequencies_from_event(
    center_factory, activity_factory, create_frequency
):
    """from the event's side we use .frequencies"""

    _center = center_factory()
    _activity = activity_factory()
    for _ in range(3):
        create_frequency(center=_center, activity=_activity)
    event = Event.objects.filter(center=_center).first()
    assert event.frequencies.count() == 3


@pytest.mark.events
@pytest.mark.django_db
def test_list_frequencies_from_person_side(
    center_factory, activity_factory, create_frequency, create_person
):
    """from the person's side we use .event_set"""

    _center = center_factory()
    _activity = activity_factory()
    _person = Person.objects.get(user=_center.made_by)
    for _ in range(3):
        create_frequency(center=_center, activity=_activity, person=_person)

    assert _person.event_set.count() == 3


@pytest.mark.events
@pytest.mark.django_db
def test_insert_frequencies_on_event(
    center_factory, activity_factory, create_event, create_person
):
    _center = center_factory()
    _activity = activity_factory()
    persons = [
        create_person(center=_center, email=_email)
        for _email in ["a@a.com", "b@b.com", "c@c.com", "d@d.com"]
    ]

    event = create_event(center=_center, activity=_activity)
    event.frequencies.add(*persons)

    assert event.frequencies.count() == 4


@pytest.mark.events
@pytest.mark.django_db
def test_clear_frequencies_on_event(
    center_factory, activity_factory, create_event, create_person
):
    _center = center_factory()
    _activity = activity_factory()
    persons = [
        create_person(center=_center, email=_email)
        for _email in ["a@a.com", "b@b.com", "c@c.com", "d@d.com"]
    ]

    event = create_event(center=_center, activity=_activity)
    event.frequencies.add(*persons)
    event.frequencies.clear()

    assert event.frequencies.count() == 0


@pytest.mark.events
@pytest.mark.django_db
def test_remove_specific_frequency_from_event(
    center_factory, activity_factory, create_event, create_person
):
    _center = center_factory()
    _activity = activity_factory()
    persons = [
        create_person(center=_center, email=_email)
        for _email in ["a@a.com", "b@b.com", "c@c.com", "d@d.com"]
    ]

    event = create_event(center=_center, activity=_activity)
    event.frequencies.add(*persons)

    person = Person.objects.last()
    event.frequencies.remove(person)
    event.save()

    assert event.frequencies.count() == 3
