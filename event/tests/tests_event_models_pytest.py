import pytest
from event.models import Activity, Event, Frequency
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
    _center = center_factory()
    _activity = activity_factory()
    for _ in range(3):
        create_frequency(center=_center, activity=_activity)
    assert Frequency.objects.count() == 3


@pytest.mark.events
@pytest.mark.django_db
def test_list_frequencies_from_person_side(
    center_factory, activity_factory, create_frequency, create_person
):
    _center = center_factory()
    _activity = activity_factory()
    _person = Person.objects.get(user=_center.made_by)
    for _ in range(3):
        create_frequency(center=_center, activity=_activity, person=_person)

    assert _person.event_set.count() == 3


# from the event's side we use .frequencies
# from the person's side we use .event_set (or related_name set in models)

#     def test_list_frequencies_from_event_1(self):
#         """.frequencies.count()"""
#         event = Event.objects.get(activity=1)
#         self.assertEqual(event.frequencies.count(), 1)

#     def test_list_frequencies_on_persons_side(self):
#         """.event_set.count()"""
#         self.assertEqual(self.person_1.event_set.count(), 1)

#     def test_insert_frequency_on_event_1(self):
#         """.frequencies.add(obj)"""
#         event = Event.objects.get(activity=2)
#         event.frequencies.add(self.person_1)
#         self.assertEqual(event.frequencies.count(), 3)

#     def test_insert_frequencies_on_event_1(self):
#         """.frequencies.add(*list_of_objs)"""
#         event = Event.objects.get(activity=1)
#         event.frequencies.add(*[self.person_2, self.person_3])
#         self.assertEqual(event.frequencies.count(), 3)

#     def test_replace_frequencies_on_event_1(self):
#         """.frequencies.set(list_of_objs)"""
#         event = Event.objects.get(activity=1)
#         event.frequencies.set([self.person_1, self.person_3])
#         self.assertEqual(event.frequencies.count(), 2)

#     def test_clear_frequencies_on_event_2(self):
#         """.frequencies.clear()"""
#         event = Event.objects.get(activity=2)
#         event.frequencies.clear()
#         self.assertEqual(event.frequencies.count(), 0)

#     def test_remove_frequency_from_event_2(self):
#         """.frequencies.remove(obj)"""
#         event = Event.objects.get(activity=2)
#         event.frequencies.remove(self.person_3)
#         self.assertEqual(event.frequencies.count(), 1)

#     def test_remove_frequencies_from_event_2(self):
#         """.frequencies.remove(*list_of_objs)"""
#         event = Event.objects.get(activity=2)
#         event.frequencies.remove(*[self.person_2, self.person_3])
#         self.assertEqual(event.frequencies.count(), 0)

#     def test_add_frequency_on_persons_side(self):
#         """person_1 is not in event_2 (event_2 has 2 frequencies)"""
#         person = self.person_1
#         person.event_set.add(self.event_2)
#         self.assertEqual(self.event_2.frequencies.count(), 3)

#     def test_search_event(self):
#         event = Event.objects.filter(date=timezone.now()).first()
#         self.assertEqual(Event.objects.count(), 2)
