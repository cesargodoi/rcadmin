import pytest
from event.models import Activity, Event

from datetime import datetime
from django.db.models.deletion import ProtectedError
from django.contrib import auth
from django.utils import timezone
from user.models import User
from event.tests.dummy import EventDummy


@pytest.mark.django_db
def test_list_persons(center_factory, create_person):
    center = center_factory()
    for _ in range(5):
        create_person(center=center)
    assert Person.objects.count() == 5


class TestEvent(EventDummy):
    # activities
    def test_list_activities(self):
        self.assertEqual(Activity.objects.count(), 3)

    def test_list_activities_multi_date(self):
        self.assertEqual(Activity.objects.filter(multi_date=True).count(), 1)

    def test_insert_activity(self):
        new = dict(
            name="Meeting",
            multi_date=True,
        )
        Activity.objects.create(**new)
        self.assertEqual(Activity.objects.count(), 4)

    def test_update_activity(self):
        to_update = Activity.objects.get(pk=2)
        to_update.multi_date = False
        to_update.save()
        self.assertEqual(Activity.objects.filter(multi_date=False).count(), 3)

    def test_delete_activity_that_is_not_in_use(self):
        Activity.objects.get(pk=3).delete()
        self.assertEqual(Activity.objects.count(), 2)

    # events
    def test_list_events(self):
        self.assertEqual(Event.objects.count(), 2)

    def test_create_event(self):
        new = dict(
            activity=self.activity_1,
            center=self.center_1,
            date=timezone.now(),
            made_by=self.office1,
        )
        Event.objects.create(**new)
        self.assertEqual(Event.objects.count(), 3)

    def test_update_event(self):
        to_update = Event.objects.get(activity=2)
        to_update.activity = self.activity_1
        to_update.save()
        self.assertEqual(Event.objects.filter(activity=1).count(), 2)

    def test_delete_event(self):
        Event.objects.get(activity=2).delete()
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Activity.objects.count(), 3)

    # frequencies
    # event_1 has 1 frequencies -> person_1
    # event_2 has 2 frequencies -> person_2 and person_3
    # from the event's side we use .frequencies
    # from the person's side we use .event_set (or related_name set in models)
    def test_list_frequencies_from_event_1(self):
        """.frequencies.count()"""
        event = Event.objects.get(activity=1)
        self.assertEqual(event.frequencies.count(), 1)

    def test_list_frequencies_on_persons_side(self):
        """.event_set.count()"""
        self.assertEqual(self.person_1.event_set.count(), 1)

    def test_insert_frequency_on_event_1(self):
        """.frequencies.add(obj)"""
        event = Event.objects.get(activity=2)
        event.frequencies.add(self.person_1)
        self.assertEqual(event.frequencies.count(), 3)

    def test_insert_frequencies_on_event_1(self):
        """.frequencies.add(*list_of_objs)"""
        event = Event.objects.get(activity=1)
        event.frequencies.add(*[self.person_2, self.person_3])
        self.assertEqual(event.frequencies.count(), 3)

    def test_replace_frequencies_on_event_1(self):
        """.frequencies.set(list_of_objs)"""
        event = Event.objects.get(activity=1)
        event.frequencies.set([self.person_1, self.person_3])
        self.assertEqual(event.frequencies.count(), 2)

    def test_clear_frequencies_on_event_2(self):
        """.frequencies.clear()"""
        event = Event.objects.get(activity=2)
        event.frequencies.clear()
        self.assertEqual(event.frequencies.count(), 0)

    def test_remove_frequency_from_event_2(self):
        """.frequencies.remove(obj)"""
        event = Event.objects.get(activity=2)
        event.frequencies.remove(self.person_3)
        self.assertEqual(event.frequencies.count(), 1)

    def test_remove_frequencies_from_event_2(self):
        """.frequencies.remove(*list_of_objs)"""
        event = Event.objects.get(activity=2)
        event.frequencies.remove(*[self.person_2, self.person_3])
        self.assertEqual(event.frequencies.count(), 0)

    def test_add_frequency_on_persons_side(self):
        """person_1 is not in event_2 (event_2 has 2 frequencies)"""
        person = self.person_1
        person.event_set.add(self.event_2)
        self.assertEqual(self.event_2.frequencies.count(), 3)

    def test_search_event(self):
        event = Event.objects.filter(date=timezone.now()).first()
        self.assertEqual(Event.objects.count(), 2)
