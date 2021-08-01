from django.utils import timezone
from center.tests.dummy import CenterDummy
from person.models import Historic, Person


class PersonDummy(CenterDummy):
    @classmethod
    def setUpTestData(cls):
        super(PersonDummy, cls).setUpTestData()
        
        # aspects
        cls.aspect_1 = "A1"
        cls.aspect_2 = "A2"

        # status
        cls.status_1 = "LIC"
        cls.status_2 = "REM"
        cls.status_3 = "DED"
        cls.status_4 = "DIS"

        # occurrences
        cls.occurrence_1 = "DIS"
        cls.occurrence_2 = "LIC"

        # persons center_1
        person_1 = dict(
            name="Office One",
            center=cls.center_1,
            reg="0001",
            status="ACT",
        )
        cls.person_1 = Person.objects.get(user=cls.office1)
        for attr, value in person_1.items():
            setattr(cls.person_1, attr, value)
        cls.person_1.save()

        person_2 = dict(
            name="Treasury One",
            center=cls.center_1,
            reg="0002",
            status="ACT",
        )
        cls.person_2 = Person.objects.get(user=cls.treasury1)
        for attr, value in person_2.items():
            setattr(cls.person_2, attr, value)
        cls.person_2.save()

        person_3 = dict(
            name="Treasury Junior One",
            center=cls.center_1,
            reg="0003",
            status="ACT",
        )
        cls.person_3 = Person.objects.get(user=cls.treasury_jr1)
        for attr, value in person_3.items():
            setattr(cls.person_3, attr, value)
        cls.person_3.save()

        person_4 = dict(
            name="Simple User One",
            center=cls.center_1,
            reg="0004",
            status="ACT",
        )
        cls.person_4 = Person.objects.get(user=cls.user1)
        for attr, value in person_4.items():
            setattr(cls.person_4, attr, value)
        cls.person_4.save()

        # persons center_2
        person_5 = dict(
            name="Office Two",
            center=cls.center_2,
            reg="0005",
            status="ACT",
        )
        cls.person_5 = Person.objects.get(user=cls.office2)
        for attr, value in person_5.items():
            setattr(cls.person_5, attr, value)
        cls.person_5.save()

        person_6 = dict(
            name="Treasury Two",
            center=cls.center_2,
            reg="0006",
            status="ACT",
        )
        cls.person_6 = Person.objects.get(user=cls.treasury2)
        for attr, value in person_6.items():
            setattr(cls.person_6, attr, value)
        cls.person_6.save()

        person_7 = dict(
            name="Treasury Junior Two",
            center=cls.center_2,
            reg="0007",
            status="ACT",
        )
        cls.person_7 = Person.objects.get(user=cls.treasury_jr2)
        for attr, value in person_7.items():
            setattr(cls.person_7, attr, value)
        cls.person_7.save()

        person_8 = dict(
            name="Simple User Two",
            center=cls.center_2,
            reg="0008",
            status="ACT",
        )
        cls.person_8 = Person.objects.get(user=cls.user2)
        for attr, value in person_8.items():
            setattr(cls.person_8, attr, value)
        cls.person_8.save()

        
        # historics
        cls.historic_1 = Historic.objects.create(
            person=cls.person_1,
            occurrence=cls.occurrence_2,
            date=timezone.now(),
        )
        


