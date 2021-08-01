from workgroup.tests.dummy import WorkgroupDummy
from event.models import Activity, Event
from django.utils import timezone


class EventDummy(WorkgroupDummy):
    @classmethod
    def setUpTestData(cls):
        super(EventDummy, cls).setUpTestData()
        # activities
        cls.activity_1 = Activity.objects.create(name="service")
        cls.activity_2 = Activity.objects.create(
            name="conference",
            multi_date=True,
            activity_type="CNF",
        )
        cls.activity_3 = Activity.objects.create(
            name="contact",
            activity_type="CTT",
        )
        # events
        cls.event_1 = Event.objects.create(
            id=1,
            activity=cls.activity_1,
            center=cls.center_1,
            date=timezone.now(),
            made_by=cls.office1,
        )
        cls.event_2 = Event.objects.create(
            id=2,
            activity=cls.activity_2,
            center=cls.center_2,
            date=timezone.now(),
            end_date=timezone.now(),
            made_by=cls.office1,
        )
        # frequencies
        cls.event_1.frequencies.add(cls.person_1)
        cls.event_2.frequencies.set([cls.person_2, cls.person_3])
