import pytest
from event.models import Event
from person.models import Person


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
    center_factory, activity_factory, create_frequency
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
    create_center, create_user, activity_factory, create_event, create_person
):
    center = create_center(user=create_user(email="u2@mail.com"))
    activity = activity_factory()
    persons = [
        create_person(center=center, email=_email)
        for _email in ["a@a.com", "b@b.com", "c@c.com", "d@d.com"]
    ]

    event = create_event(center=center, activity=activity)
    event.frequencies.add(*persons)

    person = Person.objects.filter(user__email="a@a.com")[0]
    event.frequencies.remove(person)
    event.save()

    assert event.frequencies.count() == 3
